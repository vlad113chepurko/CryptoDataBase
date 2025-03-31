import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from client import client  # Перемещаем импорт в начало файла

# Функция для расшифровки данных
def decrypted_data(key, nonce, ciphertext):
    cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher_dec.decrypt(ciphertext).decode('utf-8')
    print("Decrypted data: ", decrypted_data)

# Функция для шифрования данных
def encrypted_data(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    data_to_send = {'key': key.hex(), 'nonce': nonce.hex(), 'ciphertext': ciphertext.hex()}  # Используем hex-формат для передачи данных

    # Отправляем данные клиенту
    client.send(json.dumps(data_to_send).encode())  # Сериализуем данные в JSON и отправляем

# Функция для хеширования и шифрования
def hashed(login, password):
    key = get_random_bytes(16)
    data = login + password
    hashed_key = hashlib.sha256(key).digest()[:16]
    encrypted_data(hashed_key, data)
