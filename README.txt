============================================================
# Secure Client-Server Communication using AES-256 Encryption

## Overview

This project demonstrates secure communication between a client and a server using Python. It provides encrypted message transmission with AES-256 encryption to ensure confidentiality and protect data from unauthorized access.

The application establishes a TCP socket connection between the client and server and encrypts all messages before transmission. The receiver decrypts the received data using the shared encryption key.

This project was developed for learning secure network communication and basic cryptography concepts.

---

## Features

- Secure client-server communication
- AES-256 encryption for message confidentiality
- Real-time encrypted message exchange
- TCP socket programming
- Automatic encryption and decryption
- Simple command-line interface
- Easy to understand Python implementation

---

## Technologies Used

- Python 3
- Socket Programming
- AES-256 Encryption
- Cryptography Library

---

## Project Structure


Secure-Client-Server/
│
├── client.py
├── server.py
├── crypto_utils.py
├── requirements.txt
├── README.md
└── screenshots/


---

## How It Works

1. Start the server.
2. Start the client.
3. The client connects to the server.
4. Every message is encrypted using AES-256.
5. The encrypted message is transmitted through the socket.
6. The receiver decrypts the message.
7. The original plaintext is displayed.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YourUsername/Secure-Client-Server.git
Move into the project
cd Secure-Client-Server
Install dependencies
pip install -r requirements.txt
Running the Project
Start the Server
python server.py
Start the Client
python client.py
Example Communication

Client


Enter Message:
Hello Server


Encrypted Message


b'7fd832caef23873...'


Server


Received Encrypted Message


b'7fd832caef23873...'


After Decryption


Hello Server


---

## Security Features

- AES-256 symmetric encryption
- Secure message transmission
- Data confidentiality
- Protection against plaintext interception
- Encrypted communication over TCP sockets

---

## Learning Outcomes

- Socket Programming
- Network Communication
- Cryptography Fundamentals
- AES Encryption
- Secure Data Transmission
- Python Networking

---

## Future Enhancements

- Graphical User Interface (Tkinter)
- Secure file transfer
- User authentication
- Digital signatures
- SSL/TLS integration
- Post-Quantum Cryptography support
- Multi-client communication
- Logging and monitoring

---

## Screenshots

Add screenshots inside the **screenshots/** folder.

Example:


screenshots/
├── server.png
├── client.png
└── communication.png


---

## Requirements


Python >= 3.10

cryptography


Install using:

```bash
pip install cryptography
Author

Ambika Korala

B.Tech – Computer Science and Engineering (Cybersecurity)
============================================================
