import socket
import json
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from kyber_sim import KyberKEM, derive_aes_key

HOST = "127.0.0.1"
PORT = 9999
BUFFER = 4096


def aes_encrypt(aes_key, plaintext):
    iv = os.urandom(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv, ciphertext


def start_client():

    kyber = KyberKEM()

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))

    raw = client_sock.recv(BUFFER)
    key_data = json.loads(raw.decode())

    server_public_key = base64.b64decode(key_data["public_key"])

    ciphertext, shared_secret = kyber.encapsulate(server_public_key)

    cipher_data = json.dumps({
        "ciphertext": base64.b64encode(ciphertext).decode()
    })

    client_sock.sendall(cipher_data.encode())

    aes_key = derive_aes_key(shared_secret)

    signal = client_sock.recv(BUFFER)

    print("\nQuantum Safe VPN Connected\n")

    while True:

        message = input("Enter message: ")

        if message.lower() == "exit":
            break

        iv, encrypted_bytes = aes_encrypt(aes_key, message)

        print("Original:", message)
        print("Encrypted:", encrypted_bytes.hex())

        msg_data = json.dumps({
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(encrypted_bytes).decode(),
            "encrypted_hex": encrypted_bytes.hex()
        })

        client_sock.sendall(msg_data.encode())

        ack_raw = client_sock.recv(BUFFER)
        ack = json.loads(ack_raw.decode())

        print(ack["message"])
        print()

    client_sock.close()


if __name__ == "__main__":
    start_client()