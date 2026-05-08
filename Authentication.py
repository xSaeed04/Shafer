import tkinter as tk
from tkinter import messagebox
from Classical import show_classical_menu
from Symmetric import show_symmetric_menu
from Asymmetric import show_rsa_page
from Hash_Mac import show_hash_page
import json, os, re

BG_COLOR = "#1E1E2F"
TEXT_COLOR = "white"
USERS_FILE = "users.json"

# ------------------------------- User Storage -------------------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)
# ------------------------------- Password Validation -------------------------------
def check_password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1

    if score <= 2: return "Weak"
    elif score <= 4: return "Medium"
    else: return "Strong"
# ------------------------------- Helper Functions -------------------------------
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()
# ------------------------------- Login Page -------------------------------
def show_login_page(root):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Shafer🔒", font=("Arial", 24, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    tk.Label(root, text="Login", font=("Arial", 16),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(root, text="Username",
             bg=BG_COLOR, fg=TEXT_COLOR).pack()

    username = tk.Entry(root, width=30)
    username.pack(pady=5)

    tk.Label(root, text="Password",
             bg=BG_COLOR, fg=TEXT_COLOR).pack()

    password = tk.Entry(root, width=30, show="*")
    password.pack(pady=5)

    def login():
        users = load_users()

        if users.get(username.get()) == password.get():
            messagebox.showinfo("Success", "Login successful")
            show_main_menu(root)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tk.Button(root, text="Login", width=20,
              bg="white", fg="black",
              command=login).pack(pady=10)

    tk.Button(root, text="Create Account", width=20,
              bg="white", fg="black",
              command=lambda: show_register_page(root)).pack(pady=5)
# ------------------------------- Register Page -------------------------------
def show_register_page(root):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Shafer🔒", font=("Arial", 24, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    tk.Label(root, text="Register", font=("Arial", 16),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(root, text="Username",bg=BG_COLOR, fg=TEXT_COLOR).pack()

    username = tk.Entry(root, width=30)
    username.pack(pady=5)

    tk.Label(root, text="Password",bg=BG_COLOR, fg=TEXT_COLOR).pack()

    password = tk.Entry(root, width=30, show="*")
    password.pack(pady=5)

    strength_label = tk.Label(root, text="Password Strength:",bg=BG_COLOR, fg=TEXT_COLOR)
    strength_label.pack(pady=5)

    def update_strength(event=None):
        strength_label.config(
            text=f"Password Strength: {check_password_strength(password.get())}"
        )

    password.bind("<KeyRelease>", update_strength)

    def register():
        users = load_users()
        user = username.get()
        pwd = password.get()

        if not user or not pwd:
            messagebox.showerror("Error", "Fill all fields")

        elif user in users:
            messagebox.showerror("Error", "User already exists")

        elif check_password_strength(pwd) != "Strong":
            messagebox.showwarning("Weak Password", "Password must be strong")

        else:
            users[user] = pwd
            save_users(users)

            messagebox.showinfo("Success", "Account created")
            show_login_page(root)

    tk.Button(root, text="Register", width=20,
              bg="white", fg="black",
              command=register).pack(pady=10)

    tk.Button(root, text="Back", width=20,
              bg="white", fg="black",
              command=lambda: show_login_page(root)).pack(pady=5)
# ------------------------------- Main Menu -------------------------------
def show_main_menu(root):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    tk.Label(root, text="Shafer🔒", font=("Arial", 24, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    tk.Label(root, text="Main Menu", font=("Arial", 16),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    tk.Button(root, text="Classical Cryptography", width=25,
              bg="white", fg="black",command=lambda: show_classical_menu(root, show_main_menu)).pack(pady=5)

    tk.Button(root, text="Symmetric Encryption", width=25,
              bg="white", fg="black",command=lambda: show_symmetric_menu(root, show_main_menu)).pack(pady=5)

    tk.Button(root, text="RSA Encryption", width=25,
              bg="white", fg="black",command=lambda: show_rsa_page(root, show_main_menu)).pack(pady=5)

    tk.Button(root, text="Hash & MAC", width=25,
              bg="white", fg="black",command=lambda: show_hash_page(root, show_main_menu)).pack(pady=5)

    tk.Button(root, text="Logout", width=25,
              bg="white", fg="black",command=lambda: show_login_page(root)).pack(pady=20)