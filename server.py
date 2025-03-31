import socket, json, pyodbc
# from Crypto.Cipher import AES

server = 'localhost'
database = 'Users'
username = ''
password = ''

dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes'

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



# def handle_decrypted(key, nonce, ciphertext):
#     cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
#     decrypted_data = cipher_dec.decrypt(ciphertext).decode('utf-8')
#     print(f"Decrypted: {decrypted_data}")

def handle_received_data(data):
    received_data = json.loads(data.decode())
    print(received_data)
    key = bytes.fromhex(received_data['key'])
    nonce = bytes.fromhex(received_data['nonce'])
    ciphertext = bytes.fromhex(received_data['ciphertext'])
    login = received_data['login']

    add_to_db(login, ciphertext)

    # handle_decrypted(key, nonce, ciphertext)
def add_to_db(login, ciphertext):
    try:
        conn_db = pyodbc.connect(dsn)
        cursor = conn_db.cursor()
        cursor.execute("INSERT INTO Users ( Login, Password ) VALUES ( ?, ? )", (login, ciphertext))

        conn_db.commit()
        cursor.close()
        conn_db.close()

        print("✅ User was added!")

    except Exception as e:
        print(f"❌ Error: {e}")

while True:
    try:
        data = conn.recv(1024)
        if not data:
            print("✅ Server is closing...")
            break
        try:
            handle_received_data(data)
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    except Exception as e:
        print(f"❌ Error: {e}")
        break

conn.close()
server.close()