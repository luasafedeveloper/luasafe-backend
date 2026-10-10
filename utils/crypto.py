from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(secret: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'mineminyee_salt_2026',
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(secret.encode()))

def encrypt_script(plain: str, secret: str = "mineminyee_master_key") -> str:
    f = Fernet(derive_key(secret))
    return f.encrypt(plain.encode()).decode()

def decrypt_script(token: str, secret: str = "mineminyee_master_key") -> str:
    f = Fernet(derive_key(secret))
    return f.decrypt(token.encode()).decode()
