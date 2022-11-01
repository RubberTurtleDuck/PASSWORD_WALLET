#!/usr/bin/env python
import json
import random
import pyperclip
from tkinter import *
from tkinter import messagebox


# ---------------------------- PASSWORD GENERATOR -------------------------------------------------------------------
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '$', '%', '&', '(', ')', '*', '+']
    num_letters = random.randint(8, 10)
    num_numbers = random.randint(4, 7)
    num_symbols = random.randint(4, 7)
    password = []
    password += [random.choice(letters) for _ in range(num_letters)]
    password += [random.choice(numbers) for _ in range(num_numbers)]
    password += [random.choice(symbols) for _ in range(num_symbols)]
    random.shuffle(password)
    final_pass = ''.join(password)
    password_entry.delete(0, END)
    password_entry.insert(0, string=final_pass)
    pyperclip.copy(final_pass)


# ---------------------------- SAVE PASSWORD ------------------------------------------------------------------------
def save_password():
    website = platform_entry.get().lower()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }
    try:
        with open("data_file.json", "r") as data_file:
            # Read old data
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data_file.json", "w") as data_file:
            # Create a new file called "data_file.json" and write the new_data to it
            json.dump(new_data, data_file, indent=4)
    else:
        # Update the data in "data_file.json" with the new_data
        data.update(new_data)
        with open("data_file.json", "w") as data_file:
            # Save updated data
            json.dump(data, data_file, indent=4)
    finally:
        platform_entry.delete(0, END)
        platform_entry.insert(0, string="App/Website")
        platform_entry.focus()
        username_entry.delete(0, END)
        username_entry.insert(0, string="Username/Email")
        password_entry.delete(0, END)
        password_entry.insert(0, string="Password")


# ---------------------------- SEARCH FOR PASSWORD ------------------------------------------------------------------
def search_password():
    website = platform_entry.get().lower()
    try:
        with open("data_file.json", "r") as data_file:
            # Read old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File not found", message="There is no credentials saved yet.")
    else:
        if website in data:
            passwd = data[website]["password"]
            user = data[website]["username"]
            messagebox.showinfo(title=website.title(), message=f"user: {user}\npassword: {passwd}")
        else:
            messagebox.showinfo(title="Password not found", message=f"There is no password saved for {website}.")


# ---------------------------- UI SETUP -----------------------------------------------------------------------------
# Window setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Lock icon
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=0, row=0, columnspan=2)

# Website/App input text box
platform_entry = Entry(width=15, fg="grey")
platform_entry.insert(0, string="App/Website")
platform_entry.focus()
platform_entry.grid(column=0, row=1, pady=2)

# Username/Email input text box
username_entry = Entry(width=25, fg="grey")
username_entry.insert(0, string="Username/Email")
username_entry.grid(column=0, row=2, columnspan=2, pady=2)

# Password input text box
password_entry = Entry(width=15, fg="grey")
password_entry.insert(0, string="Password")
password_entry.grid(column=0, row=3, pady=2)

# Generate password button
generate_button = Button(text="Generate", command=generate_password)
generate_button.grid(column=1, row=3, pady=2)

# Save password button
save_button = Button(text="Save", command=save_password)
save_button.grid(column=0, row=4, columnspan=2, pady=2)

# Search button
search_button = Button(text="Search", width=6, command=search_password)
search_button.grid(column=1, row=1, pady=2)

window.mainloop()
