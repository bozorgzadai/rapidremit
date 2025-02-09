from cryptography.fernet import Fernet
import os

# # Generate a secret key once and store it securely (do not hardcode in production)
# def generate_key():
#     key = Fernet.generate_key()
#     with open("secret.key", "wb") as key_file:
#         key_file.write(key)

# Load the secret key
def load_key():
    file_path = os.path.join("encrypt", "secret.key")
    return open(file_path, "rb").read()

# Encrypt the password
def encrypting_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypting_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

