"""
Quick sanity script - not interactive, calls the library functions
directly instead of going through the CLI's password prompts, so it can
run unattended and check everything actually works.

    python test_tool.py
"""

import os
import shutil

from src.file_handler import (
    encrypt_file, decrypt_file, encrypt_directory, decrypt_directory,
    secure_delete, WrongPasswordError,
)
from src.crypto_core import generate_random_key

TEST_DIR = "test_sandbox"


def check(condition, message):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {message}")
    assert condition, message


def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(os.path.join(TEST_DIR, "documents", "subfolder"))

    with open(os.path.join(TEST_DIR, "documents", "notes.txt"), "w") as f:
        f.write("This is a confidential note about the project budget.")

    with open(os.path.join(TEST_DIR, "documents", "subfolder", "todo.txt"), "w") as f:
        f.write("1. Finish the encryption tool\n2. Write the README\n")


def test_password_roundtrip():
    print("\n-- password-based single file --")
    original = os.path.join(TEST_DIR, "documents", "notes.txt")
    with open(original) as f:
        original_content = f.read()

    encrypted_path = encrypt_file(original, output_path=os.path.join(TEST_DIR, "notes.txt.enc"),
                                   password="correct-horse-battery-staple")
    check(os.path.exists(encrypted_path), "encrypted file was created")

    with open(encrypted_path, "rb") as f:
        encrypted_bytes = f.read()
    check(original_content.encode() not in encrypted_bytes, "plaintext is not visible in the encrypted file")

    decrypted_path = decrypt_file(encrypted_path, password="correct-horse-battery-staple",
                                   output_path=os.path.join(TEST_DIR, "notes_decrypted.txt"))
    with open(decrypted_path) as f:
        check(f.read() == original_content, "decrypted content matches the original exactly")

    print("\n-- wrong password should fail cleanly --")
    try:
        decrypt_file(encrypted_path, password="totally-wrong-password",
                      output_path=os.path.join(TEST_DIR, "should_not_exist.txt"))
        check(False, "wrong password should have raised WrongPasswordError")
    except WrongPasswordError:
        check(True, "wrong password raised WrongPasswordError as expected")


def test_tamper_detection():
    print("\n-- tampering with an encrypted file should be caught --")
    original = os.path.join(TEST_DIR, "documents", "notes.txt")
    encrypted_path = encrypt_file(original, output_path=os.path.join(TEST_DIR, "tamper_test.enc"),
                                   password="another-password")

    # flip a byte somewhere in the middle of the encrypted token
    with open(encrypted_path, "r+b") as f:
        f.seek(30)
        byte = f.read(1)
        f.seek(30)
        f.write(bytes([byte[0] ^ 0xFF]))

    try:
        decrypt_file(encrypted_path, password="another-password")
        check(False, "tampered file should have failed to decrypt")
    except WrongPasswordError:
        check(True, "tampering was detected and decryption was rejected")


def test_keyfile_roundtrip():
    print("\n-- keyfile-based encryption --")
    key = generate_random_key()
    original = os.path.join(TEST_DIR, "documents", "notes.txt")

    encrypted_path = encrypt_file(original, output_path=os.path.join(TEST_DIR, "keyfile_test.enc"), key=key)
    decrypted_path = decrypt_file(encrypted_path, key=key,
                                   output_path=os.path.join(TEST_DIR, "keyfile_decrypted.txt"))

    with open(original) as f1, open(decrypted_path) as f2:
        check(f1.read() == f2.read(), "keyfile round trip matches original content")


def test_directory_roundtrip():
    print("\n-- whole-folder encryption --")
    input_dir = os.path.join(TEST_DIR, "documents")
    encrypted_dir = os.path.join(TEST_DIR, "documents_encrypted")
    decrypted_dir = os.path.join(TEST_DIR, "documents_decrypted")

    encrypted_files = encrypt_directory(input_dir, encrypted_dir, password="folder-password-123")
    check(len(encrypted_files) == 2, "both files in the folder (including the nested one) got encrypted")

    decrypted_files = decrypt_directory(encrypted_dir, decrypted_dir, password="folder-password-123")
    check(len(decrypted_files) == 2, "both files got decrypted back")

    with open(os.path.join(input_dir, "notes.txt")) as a, \
         open(os.path.join(decrypted_dir, "notes.txt")) as b:
        check(a.read() == b.read(), "top-level file matches after round trip")

    with open(os.path.join(input_dir, "subfolder", "todo.txt")) as a, \
         open(os.path.join(decrypted_dir, "subfolder", "todo.txt")) as b:
        check(a.read() == b.read(), "nested subfolder file matches after round trip")


def test_secure_delete():
    print("\n-- secure delete --")
    dummy = os.path.join(TEST_DIR, "throwaway.txt")
    with open(dummy, "w") as f:
        f.write("delete me")
    secure_delete(dummy)
    check(not os.path.exists(dummy), "file no longer exists after secure_delete")


def run():
    setup()
    test_password_roundtrip()
    test_tamper_detection()
    test_keyfile_roundtrip()
    test_directory_roundtrip()
    test_secure_delete()
    shutil.rmtree(TEST_DIR)
    print("\nAll checks passed.")


if __name__ == "__main__":
    run()
