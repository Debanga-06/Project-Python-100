"""
The actual crypto lives here, separate from anything that touches the
filesystem. Uses Fernet (from the `cryptography` library) under the hood,
which is AES-128 in CBC mode plus an HMAC for integrity checking - so if
someone tampers with the encrypted file, or you use the wrong password,
decryption fails loudly instead of silently returning garbage.

Two ways to get a key:
  - from a password, via PBKDF2 (slow on purpose, makes brute-forcing harder)
  - a randomly generated key saved to a keyfile, for people who'd rather
    not deal with remembering a password
"""

import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16          # bytes
KDF_ITERATIONS = 480_000  # current OWASP-recommended minimum for PBKDF2-SHA256


def derive_key(password: str, salt: bytes) -> bytes:
    """Turns a human password + salt into a 32-byte key Fernet can use."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    raw_key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw_key)


def generate_random_key() -> bytes:
    """A standalone random key, for keyfile-based encryption instead of a password."""
    return Fernet.generate_key()


def encrypt_bytes(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt_bytes(token: bytes, key: bytes) -> bytes:
    """Raises cryptography.fernet.InvalidToken if the key is wrong or the data was tampered with."""
    return Fernet(key).decrypt(token)


def new_salt() -> bytes:
    return os.urandom(SALT_SIZE)
