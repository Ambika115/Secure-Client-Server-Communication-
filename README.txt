============================================================
   🔐 QUANTUM SAFE VPN using Post-Quantum Cryptography
   README - How to Run This Project
============================================================

PROJECT FILES:
  kyber_sim.py  → CRYSTALS-Kyber Key Exchange (PQC module)
  server.py     → VPN Server (receives & decrypts messages)
  client.py     → VPN Client (encrypts & sends messages)
  setup.sh      → Auto-install required libraries
  README.txt    → This file

------------------------------------------------------------
STEP 1: SETUP (Run only ONCE)
------------------------------------------------------------

Open a terminal in the project folder and run:

  bash setup.sh

OR manually:

  pip3 install pycryptodome --break-system-packages

------------------------------------------------------------
STEP 2: RUN THE PROJECT (Need 2 terminals)
------------------------------------------------------------

  Terminal 1 - Start Server FIRST:
  ---------------------------------
  cd quantum_safe_vpn
  python3 server.py

  Terminal 2 - Start Client SECOND:
  -----------------------------------
  cd quantum_safe_vpn
  python3 client.py

------------------------------------------------------------
WHAT YOU WILL SEE:
------------------------------------------------------------

SERVER OUTPUT:
  ✅ Key pair generated (Kyber)
  ✅ Client connected
  ✅ Post-Quantum public key sent
  ✅ Ciphertext received from client
  ✅ Shared secret decapsulated
  ✅ AES session key derived
  ✅ Secure tunnel established
  ✅ Encrypted message received and decrypted

CLIENT OUTPUT:
  ✅ Connected to server
  ✅ Post-Quantum key exchange initiated
  ✅ Shared secret established
  ✅ Secure tunnel created
  ✅ Messages encrypted and sent

------------------------------------------------------------
HOW IT WORKS (For Viva):
------------------------------------------------------------

1. Normal VPN uses RSA for key exchange → BREAKABLE by
   quantum computers using Shor's Algorithm.

2. Our VPN uses CRYSTALS-Kyber (NIST PQC Standard) for
   key exchange → SAFE against quantum computers.
   Kyber is based on lattice mathematics (Module-LWE),
   which Shor's Algorithm cannot break.

3. AES-256 is kept for actual data encryption because
   quantum computers CANNOT break AES currently.

Architecture:
  Client
    ↓ Kyber Key Exchange (replaces RSA)
  Shared Secret Generated
    ↓ HKDF Key Derivation
  AES-256 Session Key
    ↓ Encrypted Communication
  Server

------------------------------------------------------------


============================================================
