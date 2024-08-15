from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import pandas


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    input_password.insert(0, password)
    # Auto copy password
    pyperclip.copy(password)
    # print(f"Your password is: {password}")

    # ---------------------------- SAVE PASSWORD ------------------------------- #}


def save():
    website = input_web.get()
    email = input_email.get()
    password = input_password.get()

    store_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please feel the fields")
    else:
        try:
            with open(file="password.json", mode="r") as pass_file:
                # Read file
                data = json.load(pass_file)
        except FileNotFoundError:
            print("File dose not exist, creating new json file")
            with open(file="password.json", mode="w") as data_file:
                json.dump(store_data, data_file, indent=4)
        else:
            # Update data: works as appending, simple append will duplicate the dictionary.
            data.update(store_data)
            with open(file="password.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            # After saving data in a file, content writen need to be deleted.
            input_password.delete(0, END)
            input_web.delete(0, END)


# ---------------------------- Search Websites pass and login ------------------------------- #
def find_password():
    # pass_data = pandas.read_json("password.json")
    # pass_dict = pass_data.to_dict()

    #     for site_web in pass_dict:
    #         if site_web == input_web.get():
    #             messagebox.showinfo(title=f"{site_web}", message=f'Email: {pass_dict[f"{site_web}"]["email"]}\n'
    #                                                              f'Password: {pass_dict[f"{site_web}"]["password"]}')

    try:
        with open(file="password.json") as pass_data:
            data = json.load(pass_data)

            web_site = input_web.get()
            email = data[f"{input_web.get()}"]["email"]
            password = data[f"{input_web.get()}"]["password"]

    except FileNotFoundError:
        messagebox.showwarning(title="Opps", message="Sorry there is no file yet")
    except KeyError:
        messagebox.showwarning(title="Error", message="No such website saved")
    else:
        if web_site in data:
            messagebox.showinfo(title=f"{input_web.get()}",
                                message=f'Email: {email}\n'
                                        f'Password: {password}')

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

logo_image = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Labels
label_website = Label(text="Website: ")
label_website.grid(row=1, column=0)
label_email = Label(text="Email/Username: ")
label_email.grid(row=2, column=0)
label_password = Label(text="Password: ")
label_password.grid(row=3, column=0)

# Entry
input_web = Entry(width=36)
input_web.grid(row=1, column=1)
input_web.focus()
input_email = Entry(width=55)
input_email.grid(row=2, column=1, columnspan=2)
input_email.insert(0, "example@gmail.com")
input_password = Entry(width=36)
input_password.grid(row=3, column=1)

# Buttons
button_search = Button(text="Search", width=14, command=find_password)
button_search.grid(row=1, column=2)
button_generate = Button(text="Generate Password", command=generate_password)
button_generate.grid(row=3, column=2)
button_add = Button(text="Add", width=46, command=save)
button_add.grid(row=4, column=1, columnspan=3)

window.mainloop()
