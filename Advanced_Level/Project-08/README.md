# File Encryption Tool

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)

A command-line tool that locks up files so nobody can open them without a password (or a key file). Built for my Python 100 advanced project to cover cryptography, security, and file handling in Python.

## What this project actually does

In plain terms: you point this at a file (or a whole folder), give it a password, and it scrambles the contents into something unreadable. The only way to get the original file back is to run it again with the same password. Without the password, the file is just noise - no useful information can be pulled out of it.

Think of it like a padlock for a file instead of a physical box. You've got:
- **Encrypt** - locks a file up. The result is a new file ending in `.enc` that looks like random gibberish if you try to open it normally.
- **Decrypt** - takes a `.enc` file plus the correct password and turns it back into the original file, byte for byte identical to what you started with.

A few concrete things you can do with it:
- Encrypt a single file with a password you type in
- Encrypt an entire folder (including everything in its subfolders) in one command
- Use a randomly generated key file instead of a password, if you'd rather not type one in every time
- Get an immediate, clear error if you type the wrong password, instead of silently getting corrupted garbage back
- Get an immediate error if someone has tampered with the encrypted file - it won't decrypt into something that looks fine but is secretly altered
- Optionally wipe the original unencrypted file afterward, overwriting it with random data a few times before deleting it, instead of leaving it sitting there in plain view

It's a backend/command-line tool, no graphical interface - you run commands in a terminal. That fits the "file operations" and "security" side of things without needing a UI to demonstrate what's going on.

## How the actual encryption works

Uses the `cryptography` library's Fernet recipe, which under the hood is AES-128 in CBC mode combined with an HMAC for integrity checking. That second part matters as much as the encryption itself - it's what lets the tool notice if a file has been tampered with, rather than just decrypting corrupted data and handing it back to you without a warning.

For password mode, the password itself is never used directly as the encryption key. It goes through PBKDF2 first (480,000 rounds of SHA-256, which is the current OWASP-recommended minimum), which does two things: turns a short human-memorable password into a proper-length key, and makes brute-forcing passwords by trying millions per second computationally expensive.

Every encrypted file carries its own random salt inside it, so two files encrypted with the exact same password still come out completely different from each other - there's no way to tell just from looking at ciphertexts whether the same password was reused.

## Project layout

```
file_encryption_tool/
├── cli.py                -> the command-line interface
├── src/
│   ├── crypto_core.py     -> the actual encryption/decryption + key derivation
│   └── file_handler.py    -> reading/writing files and folders, secure delete
├── test_tool.py           -> automated test covering every feature
├── requirements.txt
└── .gitignore
```

Split the "pure crypto" logic (`crypto_core.py`) away from the "touches the filesystem" logic (`file_handler.py`) on purpose - keeps the actual cryptography easy to reason about on its own, separate from things like reading files or walking folders.

## Running it

Install the one dependency:
```
pip install -r requirements.txt
```

Encrypt a single file (it'll ask you to type and confirm a password):
```
python cli.py encrypt secret.pdf
```
This creates `secret.pdf.enc`.

Decrypt it back:
```
python cli.py decrypt secret.pdf.enc
```
This gives you `secret.pdf` again, exactly as it was.

Encrypt an entire folder at once:
```
python cli.py encrypt my_documents/
```
Creates `my_documents_encrypted/` with the same folder structure inside, every file replaced with its `.enc` version.

Prefer a key file over typing a password every time:
```
python cli.py genkey mykey.key
python cli.py encrypt secret.pdf --keyfile mykey.key
python cli.py decrypt secret.pdf.enc --keyfile mykey.key
```

Encrypt and then securely wipe the original:
```
python cli.py encrypt secret.pdf --delete-original
```

## What happens if you get it wrong

Try decrypting with the wrong password:
```
$ python cli.py decrypt secret.pdf.enc
Password: 
Error: Decryption failed - wrong password/key, or the file has been altered.
```
No half-decrypted garbage file gets written, no silent failure - just a clear error.

## Testing it

`test_tool.py` runs through every feature automatically (no typing passwords by hand) and checks each result:
```
python test_tool.py
```
It covers: normal encrypt/decrypt round trips, rejecting a wrong password, catching a deliberately corrupted file, key-file mode, whole-folder encryption with a nested subfolder, and secure delete.

## Being upfront about the limits

- **"Secure delete" is best-effort, not a guarantee.** Overwriting a file with random data a few times before deleting it makes casual recovery much harder, but modern SSDs and some filesystems (journaling, snapshots, cloud sync) can keep copies elsewhere that this tool has no way to reach or overwrite.
- **Forget the password and the data is gone.** There's no backdoor, no "reset password" option - that's the whole point of encryption actually working. Same goes for a key file: lose it, lose access.
- **Whole file gets loaded into memory at once**, so this isn't built for encrypting multi-gigabyte files efficiently. Fine for documents, photos, typical project files; would need chunked/streaming encryption for very large files.

## Things I'd add with more time

- Streaming encryption for large files instead of loading everything into memory
- A progress bar when encrypting a big folder full of files
- Support for asymmetric (public/private key) encryption alongside the password-based approach, so you could encrypt something for someone else without sharing a password
- A simple GUI wrapper (tkinter) for people who'd rather drag-and-drop than use a terminal
