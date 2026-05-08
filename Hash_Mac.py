import hashlib
import hmac
import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#1E1E2F"
TEXT_COLOR = "white"
# ------------------------------- Hash & HMAC -------------------------------
def validate_hash_text(text):
    return len(text.strip()) > 0

def validate_hmac(text, key):
    return len(text.strip()) > 0 and len(key.strip()) > 0

def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def generate_hmac(text, key):
    return hmac.new(key.encode(), text.encode(), hashlib.sha256).hexdigest()
# ------------------------------- Helper Functions -------------------------------
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def input_label(parent, text):
    tk.Label(parent, text=text, bg=BG_COLOR, fg=TEXT_COLOR).pack()

def white_button(parent, text, command, width=20, pady=5):
    tk.Button(parent, text=text, width=width, bg="white", fg="black",command=command).pack(pady=pady)
# ------------------------------- Hash & MAC Page -------------------------------
def show_hash_page(root, back_func):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="Hash & MAC", font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    input_label(frame, "Enter Text")
    text_entry = tk.Entry(frame, width=50)
    text_entry.pack(pady=5)

    input_label(frame, "Enter Key (for HMAC)")
    key_entry = tk.Entry(frame, width=50)
    key_entry.pack(pady=5)

    input_label(frame, "Result")
    result_entry = tk.Entry(frame, width=60)
    result_entry.pack(pady=10)

    def do_hash():
        text = text_entry.get()

        if not validate_hash_text(text):
            messagebox.showerror("Error", "Enter text")
            return

        result_entry.delete(0, tk.END)
        result_entry.insert(0, generate_hash(text))

    def do_hmac():
        text = text_entry.get()
        key = key_entry.get()

        if not validate_hmac(text, key):
            messagebox.showerror("Error", "Enter text and key")
            return

        result_entry.delete(0, tk.END)
        result_entry.insert(0, generate_hmac(text, key))

    white_button(frame, "Generate Hash", do_hash)
    white_button(frame, "Generate HMAC", do_hmac)
    white_button(frame, "Back", lambda: back_func(root), pady=10)