import tkinter as tk
import base64
from tkinter import messagebox

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BG_COLOR = "#1E1E2F"
TEXT_COLOR = "white"
# ------------------------------- RSA Hybrid Encryption -------------------------------
def generate_rsa_keys():
    key = RSA.generate(1024)
    return key.publickey(), key

def validate_rsa_keys(public_key, private_key):
    return public_key is not None and private_key is not None

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def hybrid_encrypt(plaintext, public_key):
    aes_key = get_random_bytes(16)

    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(
        pad(plaintext.encode("utf-8"), AES.block_size)
    )

    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    combined = cipher_aes.iv + ciphertext + encrypted_key
    return base64.b64encode(combined).decode("utf-8")

def hybrid_decrypt(encoded_data, private_key):
    data = base64.b64decode(encoded_data)

    iv = data[:16]
    encrypted_key = data[-128:]
    ciphertext = data[16:-128]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_key)

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

    return decrypted.decode("utf-8")
# ------------------------------- Helper Functions -------------------------------
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def input_label(parent, text):
    tk.Label(parent, text=text, bg=BG_COLOR, fg=TEXT_COLOR).pack()

def white_button(parent, text, command, width=25, pady=3):
    tk.Button(parent, text=text, width=width, bg="white", fg="black",command=command).pack(pady=pady)
# ------------------------------- RSA Page -------------------------------
def show_rsa_page(root, back_func):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="RSA Encryption", font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    input_label(frame, "Enter Text or Load Message.txt")
    text_entry = tk.Text(frame, width=55, height=6)
    text_entry.pack(pady=5)

    input_label(frame, "Result")
    result_entry = tk.Entry(frame, width=55)
    result_entry.pack(pady=5)

    public_key = None
    private_key = None

    def generate_keys():
        nonlocal public_key, private_key
        public_key, private_key = generate_rsa_keys()
        messagebox.showinfo("Success", "RSA keys generated")

    def load_message_file():
        try:
            content = read_file("Message.txt")
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, content)
        except:
            messagebox.showerror("Error", "Message.txt not found in project folder")

    def encrypt():
        text = text_entry.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "Enter text or load Message.txt first")
            return

        if not validate_rsa_keys(public_key, private_key):
            messagebox.showerror("Error", "Generate keys first")
            return

        encrypted = hybrid_encrypt(text, public_key)
        result_entry.delete(0, tk.END)
        result_entry.insert(0, encrypted)

    def decrypt():
        encrypted_text = text_entry.get("1.0", tk.END).strip()

        if not encrypted_text:
            messagebox.showerror("Error", "Enter encrypted text first")
            return

        if not validate_rsa_keys(public_key, private_key):
            messagebox.showerror("Error", "Generate keys first")
            return

        try:
            decrypted = hybrid_decrypt(encrypted_text, private_key)
            result_entry.delete(0, tk.END)
            result_entry.insert(0, decrypted)
        except:
            messagebox.showerror("Error", "Decryption failed")

    white_button(frame, "Generate Keys", generate_keys)
    white_button(frame, "Load Message.txt", load_message_file)
    white_button(frame, "Encrypt", encrypt)
    white_button(frame, "Decrypt", decrypt)
    white_button(frame, "Back", lambda: back_func(root), pady=10)