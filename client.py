from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import socket, hashlib, json

# <Client>
PATH = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((PATH, PORT))

print("✅ Client is running...")

# <Frame>
root = Tk()
root.geometry('315x400')
root.title('Cripto')

frm = ttk.Frame(root, padding=20)
frm.grid(column=0, row=0, sticky="nsew")

is_admin = False

# <<!Function>>
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
    submit_button = ttk.Button(frm, text="Submit", command=lambda: submit(login_entry.get(), password_entry.get(), repeat_entry.get(), is_register=True))
    submit_button.grid(column=0, row=6, pady=15)

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
    SignIn = ttk.Button(frm, text="Sign in", command=lambda: submit(login_entry.get(), password_entry.get(), None, is_register=False))
    SignIn.grid(column=0, row=6, pady=15)

    # <Switch>
    SignUp = ttk.Button(frm, text="Sign up", command=sign_up)
    SignUp.grid(column=0, row=7, pady=15)

def clear_frame():
    for widget in frm.winfo_children():
        widget.destroy()

def show_message(state, message):
    if state:
        messagebox.showinfo('Completed 😀', f'{message}')
    else:
        messagebox.showerror('Error 😈', f'{message}')

def encrypted_data(key, login, password, sign_in_state, is_admin):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))

    data_to_send = {
        'key': key.hex(),
        'nonce': nonce.hex(),
        'ciphertext': ciphertext.hex(),
        'login': login,
        'sign_in_state': sign_in_state,
        'is_admin':  is_admin
    }

    print("Sending data: ", data_to_send)
    client.send(json.dumps(data_to_send).encode())

def handle_hashing(login, password, sign_in_state, is_admin):
    salt = login.encode()
    hashed_password = PBKDF2(password, salt, dkLen=16, count=100000).hex()
    hashed_key = hashlib.sha256(salt).digest()[:16]
    encrypted_data(hashed_key, login, hashed_password, sign_in_state, is_admin)

def submit(login, password, repeat, is_register):

    if login and password:
        if is_register and password != repeat:
            show_message(False, '❌ Passwords do not match!')
        else:
            if is_register:
                show_message(True, '✅ Sign up was sent to server!')
                print(f"Login: {login}")
                handle_hashing(login, password, False, is_admin=False)
            else:
                if login == 'admin' and password == 'admin':
                    handle_hashing(login, password, sign_in_state=True, is_admin=True)
                show_message(True, '✅ Sign in data was sent to server!')
                print(f"Login: {login}")
                handle_hashing(login, password, True, is_admin=False)
    else:
        show_message(False, '❌ You must write login and password!')

# <Content>
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

SignIn = ttk.Button(frm, text="Sign in", command=lambda:submit(login_entry.get(), password_entry.get(), None, is_register=False))
SignIn.grid(column=0, row=6, pady=15)

SignUp = ttk.Button(frm, text="Sign up", command=sign_up)
SignUp.grid(column=0, row=7, pady=15)

root.mainloop()
client.close()