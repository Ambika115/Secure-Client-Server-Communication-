#!/bin/bash
# ============================================================
#  setup.sh  -  Auto Setup Script for Quantum Safe VPN
#  Run this ONCE before starting the project
# ============================================================

echo "============================================================"
echo "   🔐 QUANTUM SAFE VPN - Setup Script"
echo "   Installing required Python libraries..."
echo "============================================================"
echo ""

# Update pip
echo "[1/3] Updating pip..."
pip3 install --upgrade pip --break-system-packages 2>/dev/null || pip install --upgrade pip

# Install pycryptodome (for AES)
echo ""
echo "[2/3] Installing pycryptodome (AES-256 library)..."
pip3 install pycryptodome --break-system-packages 2>/dev/null || pip install pycryptodome

echo ""
echo "[3/3] Verifying installation..."
python3 -c "from Crypto.Cipher import AES; print('  ✅ pycryptodome installed successfully!')"

echo ""
echo "============================================================"
echo "  ✅ Setup complete! You can now run the project."
echo ""
echo "  HOW TO RUN:"
echo "  Open 2 terminals in this folder, then:"
echo ""
echo "  Terminal 1 (Server):  python3 server.py"
echo "  Terminal 2 (Client):  python3 client.py"
echo "============================================================"
