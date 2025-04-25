#PDF_Cracker.py

# Importing necessary libraries
import pikepdf  # Library for handling PDF files
from tqdm import tqdm  # For displaying progress bars in the terminal
import itertools  # For generating password combinations
import string  # For predefined character sets (letters, digits, punctuation)
from concurrent.futures import ThreadPoolExecutor  # For multithreading to speed up the process

# Step 1: Function to generate passwords dynamically based on character set and length range
def generate_passwords(chars, min_length, max_length):
    # Looping over all password lengths in the specified range
    for length in range(min_length, max_length + 1):
        # Generating all possible combinations for the given length
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)  # Yield each password one by one

# Step 2: Function to load passwords from a wordlist file
def load_passwords(wordlist_file):
    with open(wordlist_file, 'r') as file:
        # Yield each line from the wordlist file as a password
        for line in file:
            yield line.strip()  # Removing any extra spaces or newlines

# Step 3: Function to attempt opening the PDF with a given password
def try_password(pdf_file, password):
    try:
        # Attempt to open the PDF with the provided password
        with pikepdf.open(pdf_file, password=password) as pdf:
            print("[+] Password found:", password)  # If successful, print the password
            return password  # Return the correct password
    except pikepdf._core.PasswordError:
        return None  # If incorrect, return None

# Step 4: Function to decrypt the PDF using the generated passwords or wordlist
def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    # Creating a progress bar for displaying decryption progress
    with tqdm(total=total_passwords, desc="Decrypting PDF", unit="password") as pbar:
        # Using ThreadPoolExecutor for parallel processing (multithreading)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submitting each password attempt to the thread pool
            future_to_password = {executor.submit(try_password, pdf_file, pwd): pwd for pwd in passwords}

            # Iterating through each password and checking if the result is successful
            for future in tqdm(future_to_password, total=total_passwords):
                password = future_to_password[future]  # Retrieving the password
                if future.result():  # If password is found, break and return the password
                    return future.result()
                pbar.update(1)  # Update the progress bar

    print("Unable to decrypt PDF. Password not found in the wordlist.")  # If no password is found, notify the user
    return None  # Return None if password was not found

# Step 5: Main function to handle command-line arguments and execute the script
if __name__ == "__main__":
    import argparse  # For handling command-line arguments

    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Decrypt a password-protected PDF file.')
    parser.add_argument('pdf_file', help='Path to the password-protected PDF file')  # Path to the PDF
    parser.add_argument('--wordlist', help='Path to the password list file', default=None)  # Path to wordlist
    parser.add_argument('--generate', action='store_true', help='Generate passwords on the fly')  # Flag for password generation
    parser.add_argument('--min_length', type=int, help='Minimum length of passwords to generate', default=1)  # Min length for generated passwords
    parser.add_argument('--max_length', type=int, help='Maximum length of passwords to generate', default=3)  # Max length for generated passwords
    parser.add_argument('--charset', type=str, help='Characters to use for password generation', default=string.ascii_letters + string.digits + string.punctuation)  # Character set for generated passwords
    parser.add_argument('--max_workers', type=int, help='Maximum number of parallel threads', default=4)  # Number of threads for parallel processing

    args = parser.parse_args()  # Parse the arguments

    # Step 6: Deciding whether to generate passwords or use the wordlist based on user input
    if args.generate:
        # If generating passwords, call the generate_passwords function
        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = sum(1 for _ in generate_passwords(args.charset, args.min_length, args.max_length))  # Count the total passwords
    elif args.wordlist:
        # If using a wordlist, load the passwords from the file
        passwords = load_passwords(args.wordlist)
        total_passwords = sum(1 for _ in load_passwords(args.wordlist))  # Count the total passwords in the wordlist
    else:
        # If neither wordlist nor password generation option is provided, exit with an error message
        print("Either --wordlist must be provided or --generate must be specified.")
        exit(1)

    # Step 7: Attempting to decrypt the PDF using the passwords and multithreading
    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)

    # Step 8: Print the result
    if decrypted_password:
        # If the password was found, print it
        print("PDF decrypted successfully with password:", decrypted_password)
    else:
        # If the password wasn't found, notify the user
        print("Unable to decrypt PDF. Password not found.")
