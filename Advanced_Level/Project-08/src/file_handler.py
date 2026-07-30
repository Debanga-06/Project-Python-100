"""
Handles the actual reading and writing of files, building on top of
crypto_core.py for the encryption itself. Also has the directory-walking
logic so you can point this at a whole folder and it just encrypts
everything inside, keeping the same folder structure.

File format for anything this tool produces (a ".enc" file):

    byte 0        -> mode: 1 = password-based, 2 = keyfile-based
    next 16 bytes -> salt (only present for mode 1, skipped for mode 2)
    everything after that -> the Fernet-encrypted token

Keeping the salt inside the file itself means you don't have to remember
to keep a separate salt file around - the encrypted file is fully
self-contained, you just need the password (or keyfile) to open it back up.
"""

import os
from cryptography.fernet import InvalidToken

from src.crypto_core import derive_key, encrypt_bytes, decrypt_bytes, new_salt, generate_random_key

MODE_PASSWORD = 1
MODE_KEYFILE = 2
ENCRYPTED_EXTENSION = ".enc"


class WrongPasswordError(Exception):
    """Raised when decryption fails - wrong password/key, or the file was tampered with."""
    pass


# ---------- single file operations ----------

def encrypt_file(input_path: str, output_path: str = None, password: str = None, key: bytes = None) -> str:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"No such file: {input_path}")
    if not password and not key:
        raise ValueError("Provide either a password or a key.")

    output_path = output_path or (input_path + ENCRYPTED_EXTENSION)

    with open(input_path, "rb") as f:
        plaintext = f.read()

    if password:
        salt = new_salt()
        derived_key = derive_key(password, salt)
        token = encrypt_bytes(plaintext, derived_key)
        header = bytes([MODE_PASSWORD]) + salt
    else:
        token = encrypt_bytes(plaintext, key)
        header = bytes([MODE_KEYFILE])

    with open(output_path, "wb") as f:
        f.write(header + token)

    return output_path


def decrypt_file(input_path: str, output_path: str = None, password: str = None, key: bytes = None) -> str:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"No such file: {input_path}")
    if not password and not key:
        raise ValueError("Provide either a password or a key.")

    with open(input_path, "rb") as f:
        raw = f.read()

    mode = raw[0]
    if mode == MODE_PASSWORD:
        if not password:
            raise ValueError("This file was encrypted with a password - a keyfile won't open it.")
        salt = raw[1:17]
        token = raw[17:]
        derived_key = derive_key(password, salt)
        actual_key = derived_key
    elif mode == MODE_KEYFILE:
        if not key:
            raise ValueError("This file was encrypted with a keyfile - a password won't open it.")
        token = raw[1:]
        actual_key = key
    else:
        raise ValueError("Unrecognized file format - is this actually a .enc file from this tool?")

    try:
        plaintext = decrypt_bytes(token, actual_key)
    except InvalidToken:
        raise WrongPasswordError("Decryption failed - wrong password/key, or the file has been altered.")

    if output_path is None:
        if input_path.endswith(ENCRYPTED_EXTENSION):
            output_path = input_path[: -len(ENCRYPTED_EXTENSION)]
        else:
            output_path = input_path + ".decrypted"

    with open(output_path, "wb") as f:
        f.write(plaintext)

    return output_path


# directory operations 

def encrypt_directory(input_dir: str, output_dir: str, password: str = None, key: bytes = None) -> list:
    """Walks input_dir, encrypts every file, mirrors the folder structure into output_dir."""
    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"No such directory: {input_dir}")

    results = []
    for root, _, files in os.walk(input_dir):
        rel_root = os.path.relpath(root, input_dir)
        target_root = os.path.join(output_dir, rel_root) if rel_root != "." else output_dir
        os.makedirs(target_root, exist_ok=True)

        for filename in files:
            src = os.path.join(root, filename)
            dst = os.path.join(target_root, filename + ENCRYPTED_EXTENSION)
            encrypt_file(src, dst, password=password, key=key)
            results.append(dst)

    return results


def decrypt_directory(input_dir: str, output_dir: str, password: str = None, key: bytes = None) -> list:
    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"No such directory: {input_dir}")

    results = []
    for root, _, files in os.walk(input_dir):
        rel_root = os.path.relpath(root, input_dir)
        target_root = os.path.join(output_dir, rel_root) if rel_root != "." else output_dir
        os.makedirs(target_root, exist_ok=True)

        for filename in files:
            if not filename.endswith(ENCRYPTED_EXTENSION):
                continue  # skip anything that isn't one of ours
            src = os.path.join(root, filename)
            dst = os.path.join(target_root, filename[: -len(ENCRYPTED_EXTENSION)])
            decrypt_file(src, dst, password=password, key=key)
            results.append(dst)

    return results


# secure-ish deletion 

def secure_delete(path: str, passes: int = 3):
    """
    Overwrites a file with random bytes a few times before deleting it, so
    the original content isn't just sitting there recoverable from the
    raw bytes on disk. Worth being upfront that this isn't bulletproof -
    SSDs with wear leveling and journaling filesystems can still keep
    copies elsewhere that this can't reach. It's a reasonable precaution,
    not a guarantee.
    """
    if not os.path.isfile(path):
        return
    length = os.path.getsize(path)
    with open(path, "r+b") as f:
        for _ in range(passes):
            f.seek(0)
            f.write(os.urandom(length))
            f.flush()
            os.fsync(f.fileno())
    os.remove(path)
