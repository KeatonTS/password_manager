from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import os

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)
alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbol_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '/', '~', '?', '<', '>']


# ----------------------------| ACCOUNT SEARCH |------------------------------- #

def search_info():
    try:
        with open("data.json", mode='r'):
            pass
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Data file not found. \n\nPlease add a website and credentials "
                                                    "to create a file to search from.")
    else:
        with open("data.json", mode='r') as file:
            data = json.load(file)
        if web_entry.get() in data:
            messagebox.showinfo(title=web_entry.get(), message=f"Email/Username: "
                                                               f"{data[web_entry.get().title()]['Email/Username']}\n"
                                                               f"Password: {data[web_entry.get().title()]['Password']}"
                                                               f"\n\nThe password was copied to your clipboard.")
            web_entry.clipboard_clear()
            web_entry.clipboard_append(data[web_entry.get().title()]['Password'])
        else:
            messagebox.showinfo(title="Oops", message=f"No matching information for {web_entry.get()} was found.")

# ----------------------------| PASSWORD GENERATOR |------------------------------- #


def generate_password():
    pass_entry.delete(0, END)
    password = [choice(alpha_list) for let in range(6)]
    lower_let = 0
    upper_let = 0

    # Making it so there are at least 2 upper and lower case letters per password
    for letter in password:
        if letter.islower():
            lower_let += 1
        if letter.isupper():
            upper_let += 1
        if lower_let >= 4:
            letter.upper()
        if upper_let >= 4:
            letter.lower()

    [password.append(choice(num_list)) for num in range(2)]
    [password.append(choice(symbol_list)) for sym in range(2)]
    shuffle(password)
    pass_entry.insert(0, ''.join(password))

# ----------------------------| SAVE PASSWORD |------------------------------- #


def save_file():

    new_data = {
        web_entry.get().title(): {
            "Email/Username": email_user_entry.get(),
            "Password": pass_entry.get(),
        }

    }

    if len(web_entry.get()) == 0 or len(pass_entry.get()) == 0 or len(email_user_entry.get()) == 0:
        messagebox.showinfo(message="Please do not leave any fields empty!", title="Review")

    else:
        try:
            with open("data.json", mode='r') as file:
                pass
        except FileNotFoundError:
            with open("data.json", mode='w') as file:
                json.dump(new_data, file, indent=4)

        else:
            with open("data.json", mode='r') as file:
                # Reading old data
                data = json.load(file)
                # Updating old data with new data
                data.update(new_data)

            with open("data.json", mode='w') as file:
                # Saving updated data
                json.dump(data, file, indent=4)

        finally:
            web_entry.clipboard_clear()
            web_entry.clipboard_append(pass_entry.get())
            web_entry.delete(0, END)
            pass_entry.delete(0, END)
            messagebox.showinfo(title='Success!', message="Your info has been added "
                                                          "successfully and copied to your clipboard!")


# ----------------------------| UI SETUP |------------------------------- #
logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
email_user_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

website_label.grid(column=0, row=1, sticky="E")
email_user_label.grid(column=0, row=2, sticky="E")
password_label.grid(column=0, row=3, sticky="E")

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", command=save_file)
add_button.grid(column=1, row=4, columnspan=2, pady=5, sticky="EW")

search_button = Button(text="Search", command=search_info)
search_button.grid(column=2, row=1, sticky="EW")


# Inputs
web_entry = Entry(width=32)
email_user_entry = Entry(width=35)
email_user_entry.insert(0, "tskeaton94@gmail.com")
pass_entry = Entry(width=32)
web_entry.focus()

web_entry.grid(column=1, row=1, columnspan=1, sticky="W")
email_user_entry.grid(column=1, row=2, columnspan=2, sticky="EW", pady=4)
pass_entry.grid(column=1, row=3, sticky="W")

window.mainloop()
