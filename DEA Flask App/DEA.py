from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64

class DEA:
    def __init__(self, encryption_type='AES', key_size=256, salt=None):
        self.backend = default_backend()
        self.encryption_type = encryption_type
        self.key_size = key_size
        self.salt = salt or os.urandom(16)

        if encryption_type == 'AES':
            self.key = os.urandom(int(self.key_size / 8))  # Generate random AES key
        elif encryption_type == 'RSA':
            # Generate RSA key pair (private and public keys)
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=self.backend)
            self.public_key = self.private_key.public_key()

    # Symmetric Key Encryption (AES)
    def aes_encrypt(self, plaintext: bytes) -> bytes:
        iv = os.urandom(16) # Initialization Vector for CBC Mode
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Padding plaintext to block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext)



    # Asymmetric Encryption (RSA)
    def rsa_encrypt(self, plaintext: bytes) -> bytes:
        encrypted = self.public_key.encrypt(
            plaintext,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted)
    


    