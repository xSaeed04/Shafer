import tkinter as tk
from tkinter import messagebox
import base64

from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

BG_COLOR = "#1E1E2F"
TEXT_COLOR = "white"
# ------------------------------- AES -------------------------------
def aes_encrypt(plaintext):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)

    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    combined = cipher.iv + ciphertext

    encrypted_text = base64.b64encode(combined).decode("utf-8")
    encoded_key = base64.b64encode(key).decode("utf-8")

    return encrypted_text, encoded_key

def aes_decrypt(encoded_text, encoded_key):
    key = base64.b64decode(encoded_key)
    data = base64.b64decode(encoded_text)

    iv = data[:16]
    ciphertext = data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode("utf-8")

def validate_aes_key(encoded_key):
    try:
        key = base64.b64decode(encoded_key, validate=True)
        return len(key) == 16
    except:
        return False
# ------------------------------- DES -------------------------------
def des_encrypt(plaintext):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC)

    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), DES.block_size))
    combined = cipher.iv + ciphertext

    encrypted_text = base64.b64encode(combined).decode("utf-8")
    encoded_key = base64.b64encode(key).decode("utf-8")

    return encrypted_text, encoded_key

def des_decrypt(encoded_text, encoded_key):
    key = base64.b64decode(encoded_key)
    data = base64.b64decode(encoded_text)

    iv = data[:8]
    ciphertext = data[8:]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)

    return decrypted.decode("utf-8")

def validate_des_key(encoded_key):
    try:
        key = base64.b64decode(encoded_key, validate=True)
        return len(key) == 8
    except:
        return False
# ------------------------------- Helper Functions -------------------------------
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def page_title(root, title):
    root.configure(bg=BG_COLOR)
    tk.Label(root, text=title, font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

def input_label(parent, text):
    tk.Label(parent, text=text, bg=BG_COLOR, fg=TEXT_COLOR).pack()

def white_button(parent, text, command, width=20, pady=5):
    tk.Button(parent, text=text, width=width, bg="white", fg="black",command=command).pack(pady=pady)
# ------------------------------- Symmetric Menu -------------------------------
def show_symmetric_menu(root, back_func):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="Symmetric Encryption", font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    white_button(frame, "AES", lambda: show_aes_page(root, back_func), width=25)
    white_button(frame, "DES", lambda: show_des_page(root, back_func), width=25)
    white_button(frame, "Back", lambda: back_func(root), width=25, pady=10)
# ------------------------------- AES Page -------------------------------
def show_aes_page(root, back_func):
    clear_window(root)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="AES Encryption", font=("Arial", 18, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    input_label(frame, "Enter Text / Encrypted Text")
    text_entry = tk.Entry(frame, width=55)
    text_entry.pack(pady=5)

    input_label(frame, "Enter Key for Decryption")
    key_entry = tk.Entry(frame, width=55)
    key_entry.pack(pady=5)

    input_label(frame, "Result")
    result_entry = tk.Entry(frame, width=60)
    result_entry.pack(pady=5)

    input_label(frame, "Key")
    key_output_entry = tk.Entry(frame, width=60)
    key_output_entry.pack(pady=5)

    def encrypt():
        text = text_entry.get()

        if not text:
            messagebox.showerror("Error", "Please enter text")
            return

        encrypted, key = aes_encrypt(text)

        result_entry.delete(0, tk.END)
        result_entry.insert(0, encrypted)

        key_output_entry.delete(0, tk.END)
        key_output_entry.insert(0, key)

    def decrypt():
        encrypted_text = text_entry.get()
        key = key_entry.get()

        if not encrypted_text or not key:
            messagebox.showerror("Error", "Please enter encrypted text and key")
            return

        if not validate_aes_key(key):
            messagebox.showerror("Error", "Invalid AES key")
            return

        try:
            decrypted = aes_decrypt(encrypted_text, key)
            result_entry.delete(0, tk.END)
            result_entry.insert(0, decrypted)
        except:
            messagebox.showerror("Error", "Decryption failed")

    white_button(frame, "Encrypt", encrypt)
    white_button(frame, "Decrypt", decrypt)
    white_button(frame, "Back", lambda: show_symmetric_menu(root, back_func), pady=10)
# ------------------------------- DES Page -------------------------------
def show_des_page(root, back_func):
    clear_window(root)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="DES Encryption", font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    input_label(frame, "Enter Text / Encrypted Text")
    text_entry = tk.Entry(frame, width=55)
    text_entry.pack(pady=5)

    input_label(frame, "Enter Key for Decryption")
    key_entry = tk.Entry(frame, width=55)
    key_entry.pack(pady=5)

    input_label(frame, "Result")
    result_entry = tk.Entry(frame, width=55)
    result_entry.pack(pady=5)

    input_label(frame, "Key")
    key_output = tk.Entry(frame, width=55)
    key_output.pack(pady=5)

    def encrypt():
        text = text_entry.get()

        if not text:
            messagebox.showerror("Error", "Enter text")
            return

        encrypted, key = des_encrypt(text)

        result_entry.delete(0, tk.END)
        result_entry.insert(0, encrypted)

        key_output.delete(0, tk.END)
        key_output.insert(0, key)

    def decrypt():
        encrypted_text = text_entry.get()
        key = key_entry.get()

        if not encrypted_text or not key:
            messagebox.showerror("Error", "Please enter encrypted text and key")
            return

        if not validate_des_key(key):
            messagebox.showerror("Error", "Invalid DES key")
            return

        try:
            decrypted = des_decrypt(encrypted_text, key)
            result_entry.delete(0, tk.END)
            result_entry.insert(0, decrypted)
        except:
            messagebox.showerror("Error", "Decryption failed")

    white_button(frame, "Encrypt", encrypt)
    white_button(frame, "Decrypt", decrypt)
    white_button(frame, "Back", lambda: show_symmetric_menu(root, back_func), pady=10)