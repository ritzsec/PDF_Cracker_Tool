# PDF_Cracker Tool 

## 🎯 Objective

The PDF Cracker Tool is designed to automate the process of attempting to decrypt a password-protected PDF file. Using either a pre-existing wordlist or generating passwords on the fly, this tool employs a brute-force approach to find the correct password for a given PDF. It leverages multithreading to speed up the decryption process by trying multiple passwords concurrently.

### 🧠 Skills Learned

- Working with the pikepdf library for decrypting PDF files.
- Understanding of brute-force password cracking methods.
- How to generate passwords programmatically using itertools.
- Implementing multithreading using ThreadPoolExecutor to speed up the process.
- Using tqdm to display progress bars in command-line applications.
- Command-line argument parsing with argparse.

### 🛠 Tools Used

- **pikepdf**: A Python library to open, read, and decrypt PDF files.
- **tqdm**: A library to create progress bars in Python.
- **itertools**: Used for generating all possible combinations of passwords from a character set.
- **argparse**: For handling command-line arguments.

## 🛠 Step-by-Step Code Breakdown

### **Step 1**:  Import Necessary Libraries
```python
import pikepdf  # For decrypting PDFs
from tqdm import tqdm  # For progress bars
import itertools  # For generating password combinations
import string  # To use built-in character sets like ascii_letters and digits
from concurrent.futures import ThreadPoolExecutor  # For parallel execution
```

### **Step 2**: Generate Passwords Dynamically
This function generates all possible combinations of passwords based on a given character set and length range.
```python
def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)
```

### **Step 3**: Load Passwords from a Wordlist
This function generates all possible combinations of passwords based on a given character set and length range.
```python
def generate_passwords(chars, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)
```

### **Step 4**: Attempt to Open the PDF with a Password
This function tries to open the PDF with the given password. If the password is correct, it will return the password; otherwise, it returns **None**.
```python
def try_password(pdf_file, password):
    try:
        # Attempt to open the PDF with the given password
        with pikepdf.open(pdf_file, password=password) as pdf:
            print("[+] Password found:", password)  # If successful, print the password
            return password
    except pikepdf._core.PasswordError:
        return None  # If the password is incorrect, return None
```

### **Step 5**: Decrypt the PDF Using Parallel Processing.
This function manages the password-cracking process using a thread pool for parallelism. It uses ThreadPoolExecutor to submit password attempts in parallel, which helps speed up the cracking process.
```python
def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    with tqdm(total=total_passwords, desc="Decrypting PDF", unit="password") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit password attempts to the executor
            future_to_password = {executor.submit(try_password, pdf_file, pwd): pwd for pwd in passwords}

            for future in tqdm(future_to_password, total=total_passwords):
                password = future_to_password[future]
                # If the password is found, return it
                if future.result():
                    return future.result()
                pbar.update(1)  # Update the progress bar

    print("Unable to decrypt PDF. Password not found in the wordlist.")
    return None  # Return None if the password is not found
```

### **Step 6**:  Main Function for Command-Line Argument Parsing.
This function parses command-line arguments using argparse, loads either the generated passwords or wordlist, and then calls the decrypt_pdf function to attempt to crack the PDF password.
```python
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Decrypt a password-protected PDF file.')
    parser.add_argument('pdf_file', help='Path to the password-protected PDF file')
    parser.add_argument('--wordlist', help='Path to the password list file', default=None)
    parser.add_argument('--generate', action='store_true', help='Generate passwords on the fly')
    parser.add_argument('--min_length', type=int, help='Minimum length of passwords to generate', default=1)
    parser.add_argument('--max_length', type=int, help='Maximum length of passwords to generate', default=3)
    parser.add_argument('--charset', type=str, help='Characters to use for password generation', default=string.ascii_letters + string.digits + string.punctuation)
    parser.add_argument('--max_workers', type=int, help='Maximum number of parallel threads', default=4)

    args = parser.parse_args()

    if args.generate:
        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = sum(1 for _ in generate_passwords(args.charset, args.min_length, args.max_length))
    elif args.wordlist:
        passwords = load_passwords(args.wordlist)
        total_passwords = sum(1 for _ in load_passwords(args.wordlist))
    else:
        print("Either --wordlist must be provided or --generate must be specified.")
        exit(1)

    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)
    
    if decrypted_password:
        print("PDF decrypted successfully with password:", decrypted_password)
    else:
        print("Unable to decrypt PDF. Password not found.")
```

### **Step 7**:  Run the Script
  print("Unable to decrypt PDF. Password not found.")




## 🛠 File Structure
```
│
├── wordlist.txt          # Your wordlist file for password cracking
├── decrypted_output.pdf  # Output decrypted PDF (if the password is found)
└── pdf_cracker.py        # The Python script for cracking the PDF password

```

## 📖 Overall Explanation 
```
This tool offers two ways to crack the password of a PDF:

      - Wordlist-based cracking: The tool uses a user-provided wordlist of passwords and tries each one on the target PDF.
      - Password generation: The tool can generate all possible passwords within a specified character set and length range.

The tool uses multithreading to try passwords concurrently, improving efficiency when dealing with large wordlists or password sets. The tqdm library is used to show a progress bar during the process, giving the user a real-time update on the decryption progress.
```

## ⚠️ Disclaimer

This tool is intended for personal use and authorized testing only.
Do not use it on any PDFs that you do not own or have explicit permission to decrypt.
Unauthorized decryption of PDF files may be illegal and unethical.


## 👤 Author

Made with curiosity and caffeine ☕  
**Gumbo**  
[GitHub Profile](https://github.com/your-username)

