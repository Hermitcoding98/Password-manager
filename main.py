from tkinter import *
from tkinter import messagebox
import string
from random import randint, choice
import pyperclip
import json


# -----------------save password------------------
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops", message="dont leave any field empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            is_ok = messagebox.askokcancel(title=website, message=f" you want to save this information?\n"
                                                                          f"Email:{email}\n"
                                                                          f"Password:{password}\n")
            if is_ok:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

        else:
            if website in data:
                email_saved = data[website]["email"]
                password_saved = data[website]["password"]
                answer = messagebox.askyesnocancel(title=website, message=f" you have this site before\n"
                                                                          f"Email:{email_saved}\n"
                                                                          f"Password:{password_saved}\n"
                                                                          f"want to replace with new pass?(no to use old pass again)", default='yes')
                if answer:
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    pyperclip.copy(password_saved)
                elif answer is None:
                    pass
                else:
                    pyperclip.copy(password_saved)
                    
            else:
                is_ok = messagebox.askokcancel(title=website, message=f" you want to save this information?\n"
                                                                          f"Email:{email}\n"
                                                                          f"Password:{password}\n")
                if is_ok:
                    data.update(new_data)
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    pyperclip.copy(password)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ----------- generate password--------

def gen_pass():
    password_entry.delete(0, END)
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(characters) for x in range(randint(10, 16)))
    password_entry.insert(0, password)


# ---------------------------Find Pass----------------------
def find_pass():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                is_ok = messagebox.askokcancel(title=website, message=f"Email:{email}\n"
                                                                      f"Password:{password}")
                if is_ok:
                    pyperclip.copy(password)
            else:
                messagebox.showinfo(title=website, message=f"The info from website: {website} not found")

    except FileNotFoundError:
        messagebox.showinfo(message="the file not found")


# --------------------main window--------------

window = Tk()
window.title("password manager")
window.config(padx=50, pady=50)
# window.geometry("700x400")


# --------logo-------
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# -------------------- label--------------------

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# --------------------Entry---------------

website_entry = Entry(width=25)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=56)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "hermitcoding98@gmail.com")
password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

# ------------------button----------------------

search_button = Button(text="search", width=25, command=find_pass)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", width=25, command=gen_pass)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=42, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
