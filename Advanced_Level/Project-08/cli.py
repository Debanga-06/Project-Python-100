"""
Command-line front end for the whole tool.

Examples:
    # password-based, single file
    python cli.py encrypt secret.pdf
    python cli.py decrypt secret.pdf.enc

    # keyfile-based (generate a key once, reuse it)
    python cli.py genkey mykey.key
    python cli.py encrypt secret.pdf --keyfile mykey.key
    python cli.py decrypt secret.pdf.enc --keyfile mykey.key

    # whole folder at once
    python cli.py encrypt my_documents/ --output encrypted_documents/

    # wipe the original after encrypting (best-effort secure delete)
    python cli.py encrypt secret.pdf --delete-original
"""

import argparse
import getpass
import os
import sys

from src.file_handler import (
    encrypt_file, decrypt_file, encrypt_directory, decrypt_directory,
    secure_delete, WrongPasswordError,
)
from src.crypto_core import generate_random_key


def get_password(confirm: bool = False) -> str:
    pw = getpass.getpass("Password: ")
    if confirm:
        pw2 = getpass.getpass("Confirm password: ")
        if pw != pw2:
            print("Passwords didn't match.", file=sys.stderr)
            sys.exit(1)
    return pw


def load_keyfile(path: str) -> bytes:
    if not os.path.isfile(path):
        print(f"Keyfile not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        return f.read().strip()


def cmd_genkey(args):
    key = generate_random_key()
    with open(args.path, "wb") as f:
        f.write(key)
    print(f"New key written to {args.path}")
    print("Keep this file safe - anyone with it can decrypt files made with it, and losing it means losing the data.")


def cmd_encrypt(args):
    password = None
    key = None

    if args.keyfile:
        key = load_keyfile(args.keyfile)
    else:
        password = get_password(confirm=True)

    try:
        if os.path.isdir(args.path):
            output_dir = args.output or (args.path.rstrip("/\\") + "_encrypted")
            results = encrypt_directory(args.path, output_dir, password=password, key=key)
            print(f"Encrypted {len(results)} file(s) into {output_dir}/")
        else:
            output_path = encrypt_file(args.path, args.output, password=password, key=key)
            print(f"Encrypted -> {output_path}")

            if args.delete_original:
                secure_delete(args.path)
                print(f"Original file securely deleted: {args.path}")

    except (FileNotFoundError, NotADirectoryError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_decrypt(args):
    password = None
    key = None

    if args.keyfile:
        key = load_keyfile(args.keyfile)
    else:
        password = get_password(confirm=False)

    try:
        if os.path.isdir(args.path):
            output_dir = args.output or (args.path.rstrip("/\\") + "_decrypted")
            results = decrypt_directory(args.path, output_dir, password=password, key=key)
            print(f"Decrypted {len(results)} file(s) into {output_dir}/")
        else:
            output_path = decrypt_file(args.path, args.output, password=password, key=key)
            print(f"Decrypted -> {output_path}")

    except WrongPasswordError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, NotADirectoryError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="file-encryption-tool",
        description="Encrypt and decrypt files or whole folders from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_encrypt = subparsers.add_parser("encrypt", help="Encrypt a file or a folder")
    p_encrypt.add_argument("path", help="File or folder to encrypt")
    p_encrypt.add_argument("-o", "--output", help="Where to write the result (default: alongside the input)")
    p_encrypt.add_argument("-k", "--keyfile", help="Use a keyfile instead of a password")
    p_encrypt.add_argument("--delete-original", action="store_true",
                            help="Securely wipe the original file after encrypting it (single files only)")
    p_encrypt.set_defaults(func=cmd_encrypt)

    p_decrypt = subparsers.add_parser("decrypt", help="Decrypt a file or a folder")
    p_decrypt.add_argument("path", help="File or folder to decrypt")
    p_decrypt.add_argument("-o", "--output", help="Where to write the result (default: alongside the input)")
    p_decrypt.add_argument("-k", "--keyfile", help="Use a keyfile instead of a password")
    p_decrypt.set_defaults(func=cmd_decrypt)

    p_genkey = subparsers.add_parser("genkey", help="Generate a random keyfile for keyfile-based encryption")
    p_genkey.add_argument("path", help="Where to save the new key")
    p_genkey.set_defaults(func=cmd_genkey)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
