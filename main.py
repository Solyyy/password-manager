from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
from cryptography.fernet import Fernet
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    global password_entry
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    final_password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, string=final_password)
    pyperclip.copy(final_password)
    messagebox.showinfo(title="Copied to Clipboard!", message="Password copied to clipboard.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():

    website_saved = website_entry.get()
    username_saved = username_entry.get()
    password_saved = password_entry.get()

    new_data = {
        website_saved: {
            "username": username_saved,
            "password": password_saved
        }
    }

    if len(website_saved) == 0 or len(password_saved) == 0 or len(username_saved) == 0:
        messagebox.showinfo(title="Oops...", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- Find PASSWORD ------------------------------- #
def find_password():

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website_entry.get() in data:
            username = data[website_entry.get()]["username"]
            password = data[website_entry.get()]["password"]
            messagebox.showinfo(title=f"{website_entry.get()}",
                                message=f"Email/Username: {username}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_entry.get()} exists")


# ---------------------------- Encrypting file ------------------------------- #
FILE = "data.json"


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()

    # encrypt data
    encrypted_data = f.encrypt(file_data)

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def encrypt_your_data():
    """This function will generate an encryption key the first time you run it. Otherwise, it will encrypt your data."""
    try:
        global KEY
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            KEY = load_key()
            encrypt(FILE, KEY)
            messagebox.showinfo(title="Success", message="Your data has been encrypted.")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No data file found, please save an Username/Password first. "
                                                   "Or your file is encrypted already.")
    # else:
    #     try:
    #         KEY = load_key()
    #     except FileNotFoundError:
    #         write_key()
    #         # load the key
    #         KEY = load_key()
    #         # encrypt it
    #         encrypt(FILE, KEY)
    #         messagebox.showinfo(title="Error",
    #                             message="Your private encryption key has been created and your data has been "
    #                                     "encrypted. Run Decrypt data to decrypt your data..")


# ---------------------------- Decrypting file ------------------------------- #
def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    messagebox.showinfo(title="Success", message="Your Data has been decrypted.")


def decrypt_your_data():
    """
    This will decrypt your data.
    """
    decrypt(FILE, KEY)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Header texts
website = Label(text="Website:")
website.grid(row=1, column=0)

username = Label(text="Email/Username:")
username.grid(row=2, column=0)

password = Label(text="Password:")
password.grid(row=3, column=0)

# Entry

website_entry = Entry()
website_entry.insert(END, string="")
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

username_entry = Entry()
username_entry.insert(END, string="test@gmail.com")
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW", pady=5)

password_entry = Entry()
password_entry.insert(END, string="")
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
password_button = Button(text="Generate Password And Copy", command=generate_password)
password_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

encrypt_your_data_button = Button(text="Encrypt Password", command=encrypt_your_data)
encrypt_your_data_button.grid(row=6, column=1, sticky="EW")

decrypt_button = Button(text="Decrypt Password", command=decrypt_your_data)
decrypt_button.grid(row=6, column=2, sticky="EW")

try:
    KEY = load_key()
except FileNotFoundError:
    question = messagebox.showinfo(title="Error", message="No encryption key found... "
                                                          "Automatically creating an encryption key.")
    write_key()

window.mainloop()
