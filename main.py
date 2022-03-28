from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Courier"
BACKGROUND_COLOR = "#DADDFC"
FOREGROUND_COLOR = "#BD4B4B"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    for letter in range(random.randint(8, 10)):
        password_list.append(random.choice(letters))

    for number in range(random.randint(2, 4)):
        password_list.append(random.choice(numbers))

    for symbol in range(random.randint(2, 4)):
        password_list.append(random.choice(symbols))

    random.shuffle(password_list)

    password_field.delete(0, END)
    password = "".join(password_list)
    password_field.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_passwords():
    website = website_field.get()
    email = email_field.get()
    password = password_field.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: " f"\nEmail: {email} "
                                                              f"\nPassword: {password}")
        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    # Reading old data.
                    data = json.load(data_file)

            except FileNotFoundError:
                print("File not found, creating a new one. Loading.......")
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating new data.
                data.update(new_data)

                with open("data.json", mode="w") as data_file:
                    # Saving updated data.
                    json.dump(data, data_file, indent=4)
            finally:
                website_field.delete(0, END)
                password_field.delete(0, END)


def find_password():
    website = website_field.get()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
                                                       f"Password: {data[website]['password']}")
        else:
            messagebox.showinfo(title="Error", message="No Account Available in Database.")


# ---------------------------- UI SETUP ------------------------------- #

# TODO: Creating window.
window = Tk()
photo = PhotoImage(file="logo.ico")
window.iconphoto(False, photo)
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# TODO: Creating a canvas.
canvas = Canvas(width=200, height=200, bg=BACKGROUND_COLOR, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# TODO: Creating labels.
website_label = Label(text="Website:", font=(FONT_NAME, 11, "bold"), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", font=(FONT_NAME, 11, "bold"), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=(FONT_NAME, 11, "bold"), bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
password_label.grid(column=0, row=3)

# TODO: Creating entries.
website_field = Entry(width=40)
website_field.focus()
website_field.grid(column=1, row=1, columnspan=2, padx=10)

email_field = Entry(width=40)
email_field.insert(0, "saher@email.com")
email_field.grid(column=1, row=2, columnspan=2, padx=10)

password_field = Entry(width=40)
password_field.grid(column=1, row=3, columnspan=2, padx=10)

# TODO: Creating buttons.
generate_password = Button(text="Random Password", command=random_password, padx=15)
generate_password.grid(column=3, row=3)

add_button = Button(text="Save", width=28, command=save_passwords, padx=20)
add_button.grid(column=1, row=4, columnspan=2)

search = Button(text="Search", width=18, command=find_password)
search.grid(column=3, row=1)

window.mainloop()
