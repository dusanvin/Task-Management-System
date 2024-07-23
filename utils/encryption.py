import os
from cryptography.fernet import Fernet

key_file_path = os.path.join("data", "key.key")
data_file_path = os.path.join("data", "data.txt")

# Function to generate a new key and save it
def generate_key():
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
    return key

# Load or generate key
if not os.path.exists(key_file_path):
    key = generate_key()
else:
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
        # Check if the key is valid
        if len(key) != 44:  # Length of a base64-encoded 32-byte key is 44 characters
            key = generate_key()

cipher_suite = Fernet(key)

# Function to load encrypted data
def load_data():
    if not os.path.exists(data_file_path):
        return []
    try:
        with open(data_file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        data = []
        for line in decrypted_data.splitlines():
            parts = line.split('|')
            if len(parts) >= 3 and parts[0] in ('0', '1'):
                if len(parts) < 5:
                    parts.extend(["", ""])  # Ensure all parts are present for backward compatibility
                data.append(parts)
            else:
                print(f"Invalid data format: {line}")
        return data
    except (Fernet.InvalidToken, ValueError) as e:
        print("Error decrypting data: ", e)
        return []

# Function to save encrypted data
def save_data(data):
    data_to_save = ["|".join(item[:5]) for item in data]
    encrypted_data = cipher_suite.encrypt("\n".join(data_to_save).encode())
    with open(data_file_path, "wb") as file:
        file.write(encrypted_data)
