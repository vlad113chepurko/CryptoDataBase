from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('315x400')
root.title('Cripto')

frm = ttk.Frame(root, padding=20)
frm.grid(column=0, row=0, sticky="nsew")

def sign_up():

    root.title('Sign up')
    clear_frame()

    # <Login/Entry>
    login_label = ttk.Label(frm, text='New login:', font='Arial 12')
    login_label.grid(column=0, row=0, sticky="w", pady=5)
    login_entry = ttk.Entry(frm, font='Arial 12', width=30)
    login_entry.grid(column=0, row=1, pady=5)

    # <Password/Entry>
    password_label = ttk.Label(frm, text='New password:', font='Arial 12')
    password_label.grid(column=0, row=2, sticky="w", pady=5)
    password_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
    password_entry.grid(column=0, row=3, pady=5)

    # <Repeat>
    repeat_label = ttk.Label(frm, text='Repeat password:', font='Arial 12')
    repeat_label.grid(column=0, row=4, sticky="w", pady=5)
    repeat_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
    repeat_entry.grid(column=0, row=5, pady=5)

    # <Submit>
    submit = ttk.Button(frm, text="Submit", command=sign_up)
    submit.grid(column=0, row=6, pady=15)

    # <Switch to login>
    SignIn = ttk.Button(frm, text="Sign in", command=sign_in)
    SignIn.grid(column=0, row=7, pady=15)

def sign_in():

    root.title('Sign in')
    clear_frame()

    # <Login/Entry>
    login_label = ttk.Label(frm, text='Login:', font='Arial 12')
    login_label.grid(column=0, row=0, sticky="w", pady=5)
    login_entry = ttk.Entry(frm, font='Arial 12', width=30)
    login_entry.grid(column=0, row=1, pady=5)

    # <Password/Entry>
    password_label = ttk.Label(frm, text='Password:', font='Arial 12')
    password_label.grid(column=0, row=2, sticky="w", pady=5)
    password_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
    password_entry.grid(column=0, row=3, pady=5)

    # <Repeat>
    repeat_label = ttk.Label(frm, text='Repeat password:', font='Arial 12')
    repeat_label.grid(column=0, row=4, sticky="w", pady=5)
    repeat_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
    repeat_entry.grid(column=0, row=5, pady=5)

    # <Submit>
    SignIn = ttk.Button(frm, text="Sign in", command=lambda: print("Sign In"))
    SignIn.grid(column=0, row=6, pady=15)

    # <Switch>
    SignUp = ttk.Button(frm, text="Sign up", command=sign_up)
    SignUp.grid(column=0, row=7, pady=15)

def clear_frame():
    for widget in frm.winfo_children():
        widget.destroy()


login_label = ttk.Label(frm, text='Login:', font='Arial 12')
login_label.grid(column=0, row=0, sticky="w", pady=5)
login_entry = ttk.Entry(frm, font='Arial 12', width=30)
login_entry.grid(column=0, row=1, pady=5)

password_label = ttk.Label(frm, text='Password:', font='Arial 12')
password_label.grid(column=0, row=2, sticky="w", pady=5)
password_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
password_entry.grid(column=0, row=3, pady=5)

repeat_label = ttk.Label(frm, text='Repeat password:', font='Arial 12')
repeat_label.grid(column=0, row=4, sticky="w", pady=5)
repeat_entry = ttk.Entry(frm, font='Arial 12', width=30, show="*")
repeat_entry.grid(column=0, row=5, pady=5)

SignIn = ttk.Button(frm, text="Sign in", command=lambda: print("Sign In"))
SignIn.grid(column=0, row=6, pady=15)

SignUp = ttk.Button(frm, text="Sign up", command=sign_up)
SignUp.grid(column=0, row=7, pady=15)

root.mainloop()