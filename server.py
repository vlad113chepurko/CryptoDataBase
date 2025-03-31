import socket, json
from Crypto.Cipher import AES

PATH = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((PATH, PORT))
server.listen(1)

print("Server is running...")

conn, addr = server.accept()
print(f"Connection from {addr} has been established!")

def handle_decrypted(key, nonce, ciphertext):
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher_dec.decrypt(ciphertext).decode('utf-8')
    print(f"Decrypted: {decrypted_data}")

def handle_received_data(data):
    received_data = json.loads(data.decode())
    key = bytes.fromhex(received_data['key'])
    nonce = bytes.fromhex(received_data['nonce'])
    ciphertext = bytes.fromhex(received_data['ciphertext'])

    handle_decrypted(key, nonce, ciphertext)

while True:

    data = conn.recv(1024)

    if not data:
        print("Server is closing...")
        break

    handle_received_data(data)

conn.close()
server.close()