import tkinter as tk
from cryptography.fernet import Fernet

# Generate a unique encryption key
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    with open('key.key', 'rb') as key_file:
        return key_file.read()

# Encrypt a password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Save the encrypted password to a text file
def save_password(username, encrypted_password):
    with open('passwords.txt', 'a') as file:
        file.write(f'{username},{encrypted_password.decode()}\n')

# Retrieve the encrypted password from the text file
def get_encrypted_password(username):
    with open('passwords.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == username:
                return parts[1].encode()
    return None

# Create a GUI for the password manager
def create_gui():
    # Callback function for saving password
    def save_password_callback():
        username = username_entry.get()
        password = password_entry.get()
        key = load_key()
        encrypted_password = encrypt_password(password, key)
        save_password(username, encrypted_password)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    # Callback function for retrieving password
    def retrieve_password_callback():
        username = username_entry.get()
        key = load_key()
        encrypted_password = get_encrypted_password(username)
        if encrypted_password:
            password = decrypt_password(encrypted_password, key)
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
        else:
            password_entry.delete(0, tk.END)
            password_entry.insert(0, "No password found.")

    # Create the main window
    window = tk.Tk()
    window.title("Password Manager")

    # Create the username label and entry
    username_label = tk.Label(window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    # Create the password label and entry
    password_label = tk.Label(window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # Create the save password button
    save_button = tk.Button(window, text="Save Password", command=save_password_callback)
    save_button.pack()

    # Create the retrieve password button
    retrieve_button = tk.Button(window, text="Retrieve Password", command=retrieve_password_callback)
    retrieve_button.pack()

    # Run the main loop
    window.mainloop()

# Entry point of the program
if __name__ == '__main__':
    generate_key()
    create_gui()
