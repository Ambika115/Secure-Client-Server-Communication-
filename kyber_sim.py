import hashlib
import secrets


class KyberKEM:

    KEY_SIZE = 32

    def __init__(self):
        self.algorithm = "CRYSTALS-Kyber (Simulation)"
        self.nist_level = "Level 3 (Kyber-768 inspired)"

    def keygen(self):
        seed = secrets.token_bytes(32)

        private_key = hashlib.sha3_512(seed + b"KYBER_PRIVATE").digest()
        public_key = hashlib.sha3_512(seed + b"KYBER_PUBLIC").digest()

        return public_key, private_key, seed

    def encapsulate(self, public_key):

        random_coin = secrets.token_bytes(32)

        shared_secret = hashlib.sha3_256(
            public_key + random_coin + b"KYBER_SHARED"
        ).digest()

        ciphertext = hashlib.sha3_512(
            public_key + random_coin + b"KYBER_CIPHER"
        ).digest() + random_coin

        return ciphertext, shared_secret

    def decapsulate(self, ciphertext, private_key, seed):

        random_coin = ciphertext[64:]

        public_key = hashlib.sha3_512(seed + b"KYBER_PUBLIC").digest()

        shared_secret = hashlib.sha3_256(
            public_key + random_coin + b"KYBER_SHARED"
        ).digest()

        return shared_secret


def derive_aes_key(shared_secret):

    aes_key = hashlib.sha256(
        shared_secret + b"AES_SESSION_KEY"
    ).digest()

    return aes_key