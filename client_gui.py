import socket
import json
import base64
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from kyber_sim import KyberKEM, derive_aes_key
from crypto_utils import encrypt_data

HOST = "127.0.0.1"
PORT = 9999
BUFFER = 4096

class SecureChatClient:

    def __init__(self):

        # 🔌 Connect to server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        kyber = KyberKEM()

        # 🔑 Receive public key
        raw = self.sock.recv(BUFFER)

        if not raw:
            print("❌ Server not responding. Start server first.")
            return

        key_data = json.loads(raw.decode())
        server_public_key = base64.b64decode(key_data["public_key"])

        # 🔐 Kyber key exchange
        ciphertext, shared_secret = kyber.encapsulate(server_public_key)

        self.sock.sendall(json.dumps({
            "ciphertext": base64.b64encode(ciphertext).decode()
        }).encode())

        # 🔑 AES key
        self.aes_key = derive_aes_key(shared_secret)

        self.sock.recv(BUFFER)

        # 🎨 UI
        self.window = tk.Tk()
        self.window.title("🔐 Quantum Secure Chat")
        self.window.geometry("600x550")
        self.window.configure(bg="#1e1e2e")

        title = tk.Label(self.window, text="Quantum Secure Chat",
                         font=("Arial", 18, "bold"),
                         bg="#1e1e2e", fg="#8be9fd")
        title.pack(pady=10)

        # 📺 Output box
        self.output = tk.Text(self.window, height=20, width=70,
                              bg="#282a36", fg="white",
                              font=("Consolas", 10))
        self.output.pack(pady=10)
        self.output.config(state=tk.DISABLED)

        # ⌨️ Input
        self.entry = tk.Entry(self.window, width=50, font=("Arial", 11))
        self.entry.pack(pady=5)

        # 🔘 Buttons
        btn_frame = tk.Frame(self.window, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Send Text",
                  command=self.send_message,
                  bg="#50fa7b", width=12).grid(row=0, column=0, padx=8)

        tk.Button(btn_frame, text="Send File",
                  command=self.send_file,
                  bg="#8be9fd", width=12).grid(row=0, column=1, padx=8)

        tk.Button(btn_frame, text="Clear",
                  command=self.clear_chat,
                  bg="#ff5555", width=12).grid(row=0, column=2, padx=8)

        self.window.mainloop()

    # 🧾 Logger
    def log(self, msg):
        time = datetime.now().strftime("%H:%M:%S")
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, f"[{time}] {msg}\n")
        self.output.config(state=tk.DISABLED)
        self.output.see(tk.END)

    # 📝 SEND TEXT
    def send_message(self):
        msg = self.entry.get().strip()
        if not msg:
            return

        iv, encrypted = encrypt_data(self.aes_key, msg.encode())

        data = {
            "type": "text",
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(encrypted).decode()
        }

        self.sock.sendall(json.dumps(data).encode())

        # 🔐 Show encrypted text
        encrypted_text = base64.b64encode(encrypted).decode()

        # 📩 Receive response
        ack = self.sock.recv(BUFFER)
        ack_msg = json.loads(ack.decode())

        self.log(f"📝 Original: {msg}")
        self.log(f"🔐 Encrypted: {encrypted_text}")
        self.log(f"✅ Server: {ack_msg['message']}")

        self.entry.delete(0, tk.END)

    # 📁 SEND FILE
    def send_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Documents", "*.pdf *.docx *.txt"),
                ("Images", "*.png *.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        with open(file_path, "rb") as f:
            file_data = f.read()

        file_name = os.path.basename(file_path)

        # 🔐 Encrypt file
        iv, encrypted = encrypt_data(self.aes_key, file_data)

        data = {
            "type": "file",
            "file_name": file_name,
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(encrypted).decode()
        }

        self.sock.sendall(json.dumps(data).encode())

        # 📩 Receive response
        ack = self.sock.recv(BUFFER)
        ack_msg = json.loads(ack.decode())

        # 🔐 Show encrypted preview (first 100 chars)
        encrypted_preview = base64.b64encode(encrypted).decode()[:100]

        size_kb = len(file_data) // 1024

        self.log(f"📁 File Sent: {file_name} ({size_kb} KB)")
        self.log(f"🔐 Encrypted Preview: {encrypted_preview}...")
        self.log(f"✅ Server: {ack_msg['message']}")

    # 🧹 CLEAR CHAT
    def clear_chat(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.config(state=tk.DISABLED)


SecureChatClient()