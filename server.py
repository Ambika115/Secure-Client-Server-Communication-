import socket
import json
import base64
import os
from kyber_sim import KyberKEM, derive_aes_key
from crypto_utils import decrypt_data

HOST = "127.0.0.1"
PORT = 9999
BUFFER = 4096

os.makedirs("received_files", exist_ok=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("🚀 Server started... Waiting for connection")

conn, addr = server.accept()
print(f"✅ Connected: {addr}")

kyber = KyberKEM()

# ✅ FIXED KEYGEN (handles extra return values like seed)
keys = kyber.keygen()
public_key = keys[0]
private_key = keys[1]
seed = keys[2]   # ⭐ IMPORTANT FIX

# Send public key to client
conn.sendall(json.dumps({
    "public_key": base64.b64encode(public_key).decode()
}).encode())

# Receive encapsulated key from client
data = conn.recv(BUFFER)
cipher_data = json.loads(data.decode())
ciphertext = base64.b64decode(cipher_data["ciphertext"])

# ✅ FIXED decapsulation (added seed)
shared_secret = kyber.decapsulate(ciphertext, private_key, seed)

# Derive AES key
aes_key = derive_aes_key(shared_secret)

conn.sendall(b"READY")

# Main communication loop
while True:
    data = conn.recv(BUFFER)
    if not data:
        break

    msg = json.loads(data.decode())

    iv = base64.b64decode(msg["iv"])
    ciphertext = base64.b64decode(msg["ciphertext"])

    decrypted = decrypt_data(aes_key, iv, ciphertext)

    if msg["type"] == "text":
        print("📝 Message:", decrypted.decode())

    elif msg["type"] == "file":
        file_name = msg["file_name"]
        file_path = os.path.join("received_files", file_name)

        with open(file_path, "wb") as f:
            f.write(decrypted)

        print(f"📁 File received: {file_name}")

    # Send acknowledgment back to client
    conn.sendall(json.dumps({
        "message": "Received successfully"
    }).encode())

conn.close()