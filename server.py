import socket, json, pyodbc
from Crypto.Cipher import AES
import hashlib

server_name = 'localhost'
database = 'Users'
username = ''
password = ''

dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes'

PATH = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((PATH, PORT))
server.listen(1)

print("✅ Server is running...")

try:
    conn, addr = server.accept()
    print(f"✅ Connection from {addr} has been established!")
except ConnectionError:
    print("❌ Error with connection!")


def handle_decrypted(key, nonce, ciphertext):
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decrypted_data = cipher_dec.decrypt(ciphertext)
        return decrypted_data
    except ValueError as e:
        print(f"❌ Decryption error: {e}")
        return None

def close_all(con, cur):
    if con:
        try:
            con.commit()
            cur.close()
            con.close()
        except Exception as e:
            print(f"❌ Error closing connection: {e}")

def handle_received_data(data):
    try:
        received_data = json.loads(data.decode())
        print(received_data)

        key = bytes.fromhex(received_data['key']) if isinstance(received_data['key'], str) else received_data['key']
        nonce = bytes.fromhex(received_data['nonce']) if isinstance(received_data['nonce'], str) else received_data['nonce']
        ciphertext = bytes.fromhex(received_data['ciphertext']) if isinstance(received_data['ciphertext'], str) else received_data['ciphertext']

        login = received_data['login']
        sign_in_state = received_data['sign_in_state']

        add_to_db(login, key, nonce, ciphertext, sign_in_state)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except KeyError as e:
        print(f"❌ Missing key in received data: {e}")

def add_to_db(login, key, nonce, ciphertext, sign_in_state):
    conn_db = None
    cursor = None
    try:
        conn_db = pyodbc.connect(dsn)
        cursor = conn_db.cursor()

        cursor.execute("SELECT Password, Nonce FROM Users WHERE Login = ?", (login,))
        row = cursor.fetchone()

        if not sign_in_state:
            if row:
                print("❌ User already exists!")
            else:
                cursor.execute("""
                    INSERT INTO Users (Login, Password, Nonce)
                    VALUES (?, ?, ?)
                """, (login, ciphertext, nonce))
                conn_db.commit()
                print("✅ User was added!")

        else:
            if row:
                stored_ciphertext = row[0]
                stored_nonce = row[1]

                decrypted_password = handle_decrypted(key, stored_nonce, stored_ciphertext)

                if decrypted_password is None:
                    print ("❌ Decryption failed, cannot log in")
                    return

                hashed_input_password = hashlib.sha256(decrypted_password).hexdigest()

                input_decrypted = handle_decrypted(key, nonce, ciphertext)

                if input_decrypted is None:
                    print ("❌ Decryption failed, cannot log in")
                    return

                if hashed_input_password == hashlib.sha256(input_decrypted).hexdigest():
                    print('✅ You have logged in successfully!')
                else:
                    print("❌ Incorrect password!")
            else:
                print("❌ User not found!")

    except pyodbc.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ General error: {e}")
    finally:
        close_all(conn_db, cursor)

while True:
    try:
        data = conn.recv(1024)
        if not data:
            print("✅ Server is closing...")
            break
        handle_received_data(data)
    except Exception as e:
        print(f"❌ Error: {e}")
        break

conn.close()
server.close()