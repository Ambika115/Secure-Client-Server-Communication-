from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_data(key, data_bytes):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data_bytes, AES.block_size))
    return iv, ciphertext

def decrypt_data(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)