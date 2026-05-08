import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#1E1E2F"
TEXT_COLOR = "white"

# ------------------------------- Caesar Cipher -------------------------------
def Ceaser_En(Plain, K):
    C = ""
    for ch in Plain.lower():
        if ch.isalpha():
            p = ord(ch) - 97
            C += chr(97 + ((p + K) % 26))
        else:
            C += ch
    return C

def Caesar_De(Cipher, K):
    P = ""
    for letter in Cipher.lower():
        if letter.isalpha():
            C = ord(letter) - 97
            P += chr(97 + ((C - K) % 26))
        else:
            P += letter
    return P

def validate_caesar_key(key):
    return key.isdigit() and 0 <= int(key) <= 25
# ------------------------------- Monoalpha Cipher -------------------------------
def Monoalpha_En(Plain, K):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    K = K.strip().lower()
    C = ""

    for ch in Plain.lower():
        if ch in alpha:
            index = alpha.find(ch)
            C += K[index]
        else:
            C += ch
    return C

def Monoalpha_De(Cipher, K):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    K = K.strip().lower()
    P = ""

    for ch in Cipher.lower():
        if ch in K:
            index = K.find(ch)
            P += alpha[index]
        else:
            P += ch
    return P

def validate_monoalpha_key(key):
    key = key.strip().lower()
    return key.isalpha() and len(key) == 26 and len(set(key)) == 26
# ------------------------------- Vigenere Cipher -------------------------------
def Vigenere_En(Plain, Key):
    C = ""
    K = Key.lower()
    key_len = len(K)
    j = 0

    for ch in Plain.lower():
        if ch.isalpha():
            p = ord(ch) - 97
            k = ord(K[j % key_len]) - 97
            C += chr(97 + ((p + k) % 26))
            j += 1
        else:
            C += ch
    return C

def Vigenere_De(Cipher, Key):
    P = ""
    K = Key.lower()
    key_len = len(K)
    j = 0

    for ch in Cipher.lower():
        if ch.isalpha():
            p = ord(ch) - 97
            k = ord(K[j % key_len]) - 97
            P += chr(97 + ((p - k) % 26))
            j += 1
        else:
            P += ch
    return P

def validate_vigenere_key(key):
    return key.strip().isalpha()
# ------------------------------- Playfair Cipher -------------------------------
def Create_Matrix(key):
    key = key.lower().replace("j", "i")
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    used = []

    for ch in key + alphabet:
        if ch.isalpha() and ch not in used:
            used.append(ch)

    matrix = []
    for i in range(5):
        matrix.append(used[i * 5:(i + 1) * 5])
    return matrix

def Split_Letters(text):
    text = text.lower().replace("j", "i")
    text = "".join(ch for ch in text if ch.isalpha())

    result = ""
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "x"

        if a == b:
            result += a + "x"
            i += 1
        else:
            result += a + b
            i += 2

    if len(result) % 2 != 0:
        result += "x"

    return result

def Find_Position(matrix, ch):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col

def Encrypt_Decrypt(text, matrix, mode):
    result = ""
    step = 1 if mode == "encrypt" else -1

    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]

        r1, c1 = Find_Position(matrix, a)
        r2, c2 = Find_Position(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1 + step) % 5]
            result += matrix[r2][(c2 + step) % 5]
        elif c1 == c2:
            result += matrix[(r1 + step) % 5][c1]
            result += matrix[(r2 + step) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result

def Playfair_En(plain, key):
    matrix = Create_Matrix(key)
    prepared = Split_Letters(plain)
    return Encrypt_Decrypt(prepared, matrix, "encrypt")

def Playfair_De(cipher, key):
    matrix = Create_Matrix(key)
    cipher = cipher.lower().replace("j", "i")
    cipher = "".join(ch for ch in cipher if ch.isalpha())

    if len(cipher) % 2 != 0:
        cipher += "x"

    return Encrypt_Decrypt(cipher, matrix, "decrypt")

def validate_playfair_key(key):
    key = key.strip()
    return key.replace(" ", "").isalpha()
# ------------------------------- Vernam Cipher -------------------------------
def vernam(text, key):
    result = ""
    text = text.upper().replace(" ", "")
    key = key.upper().replace(" ", "")

    for i in range(len(text)):
        t = ord(text[i]) - 65
        k = ord(key[i]) - 65
        c = t ^ k
        result += chr(c + 65)

    return result

def validate_vernam_key(text, key):
    text = text.replace(" ", "")
    key = key.replace(" ", "")
    return text.isalpha() and key.isalpha() and len(key) == len(text)
# ------------------------------- Helper Functions -------------------------------
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def page_title(root, title):
    root.configure(bg=BG_COLOR)
    tk.Label(root, text=title, font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

def input_label(root, text):
    tk.Label(root, text=text, bg=BG_COLOR, fg=TEXT_COLOR).pack()

def white_button(root, text, command, width=20, pady=5):
    tk.Button(root, text=text, width=width, bg="white", fg="black",command=command).pack(pady=pady)
# ------------------------------- Classical Menu -------------------------------
def show_classical_menu(root, back_func):
    clear_window(root)
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=120)

    tk.Label(frame, text="Classical Cryptography", font=("Arial", 18, "bold"),bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    tk.Button(frame, text="Caesar Cipher", width=25, bg="white", fg="black",command=lambda: show_caesar_page(root, back_func)).pack(pady=3)

    tk.Button(frame, text="Monoalpha Cipher", width=25, bg="white", fg="black",command=lambda: show_monoalpha_page(root, back_func)).pack(pady=3)

    tk.Button(frame, text="Vigenere Cipher", width=25, bg="white", fg="black",command=lambda: show_vigenere_page(root, back_func)).pack(pady=3)

    tk.Button(frame, text="Playfair Cipher", width=25, bg="white", fg="black",command=lambda: show_playfair_page(root, back_func)).pack(pady=3)

    tk.Button(frame, text="Vernam Cipher", width=25, bg="white", fg="black",command=lambda: show_vernam_page(root, back_func)).pack(pady=3)

    tk.Button(frame, text="Back", width=25, bg="white", fg="black",command=lambda: back_func(root)).pack(pady=10)
# ------------------------------- Caesar Page -------------------------------
def show_caesar_page(root, back_func):
    clear_window(root)
    page_title(root, "Caesar Cipher")

    input_label(root, "Enter Text")
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    input_label(root, "Enter Key (0-25)")
    key_entry = tk.Entry(root, width=20)
    key_entry.pack(pady=5)

    result_label = tk.Label(root, text="Result:", bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=10)

    def encrypt():
        text = text_entry.get()
        key = key_entry.get()

        if not validate_caesar_key(key):
            messagebox.showerror("Error", "Key must be a number from 0 to 25")
            return

        result_label.config(text="Result: " + Ceaser_En(text, int(key)))

    def decrypt():
        text = text_entry.get()
        key = key_entry.get()

        if not validate_caesar_key(key):
            messagebox.showerror("Error", "Key must be a number from 0 to 25")
            return

        result_label.config(text="Result: " + Caesar_De(text, int(key)))

    white_button(root, "Encrypt", encrypt)
    white_button(root, "Decrypt", decrypt)
    white_button(root, "Back", lambda: show_classical_menu(root, back_func), pady=10)
# ------------------------------- Monoalpha Page -------------------------------
def show_monoalpha_page(root, back_func):
    clear_window(root)
    page_title(root, "Monoalphabetic Cipher")

    input_label(root, "Enter Text")
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    input_label(root, "Enter Key (26 unique letters)")
    key_entry = tk.Entry(root, width=40)
    key_entry.pack(pady=5)

    result_label = tk.Label(root, text="Result:", bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=10)

    def encrypt():
        text = text_entry.get()
        key = key_entry.get().strip().lower()

        if not validate_monoalpha_key(key):
            messagebox.showerror("Error", "Key must be 26 unique letters")
            return

        result_label.config(text="Result: " + Monoalpha_En(text, key))

    def decrypt():
        text = text_entry.get()
        key = key_entry.get().strip().lower()

        if not validate_monoalpha_key(key):
            messagebox.showerror("Error", "Key must be 26 unique letters")
            return

        result_label.config(text="Result: " + Monoalpha_De(text, key))

    white_button(root, "Encrypt", encrypt)
    white_button(root, "Decrypt", decrypt)
    white_button(root, "Back", lambda: show_classical_menu(root, back_func), pady=10)
# ------------------------------- Vigenere Page -------------------------------
def show_vigenere_page(root, back_func):
    clear_window(root)
    page_title(root, "Vigenere Cipher")

    input_label(root, "Enter Text")
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    input_label(root, "Enter Key (letters only)")
    key_entry = tk.Entry(root, width=40)
    key_entry.pack(pady=5)

    result_label = tk.Label(root, text="Result:", bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=10)

    def encrypt():
        text = text_entry.get()
        key = key_entry.get().strip()

        if not validate_vigenere_key(key):
            messagebox.showerror("Error", "Key must be letters only")
            return

        result_label.config(text="Result: " + Vigenere_En(text, key))

    def decrypt():
        text = text_entry.get()
        key = key_entry.get().strip()

        if not validate_vigenere_key(key):
            messagebox.showerror("Error", "Key must be letters only")
            return

        result_label.config(text="Result: " + Vigenere_De(text, key))

    white_button(root, "Encrypt", encrypt)
    white_button(root, "Decrypt", decrypt)
    white_button(root, "Back", lambda: show_classical_menu(root, back_func), pady=10)
# ------------------------------- Playfair Page -------------------------------
def show_playfair_page(root, back_func):
    clear_window(root)
    page_title(root, "Playfair Cipher")

    input_label(root, "Enter Text")
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    input_label(root, "Enter Key (letters only)")
    key_entry = tk.Entry(root, width=40)
    key_entry.pack(pady=5)

    result_label = tk.Label(root, text="Result:", bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=10)

    def encrypt():
        text = text_entry.get()
        key = key_entry.get().strip()

        if not validate_playfair_key(key):
            messagebox.showerror("Error", "Key must be letters only")
            return

        result_label.config(text="Result: " + Playfair_En(text, key))

    def decrypt():
        text = text_entry.get()
        key = key_entry.get().strip()

        if not validate_playfair_key(key):
            messagebox.showerror("Error", "Key must be letters only")
            return

        result_label.config(text="Result: " + Playfair_De(text, key))

    white_button(root, "Encrypt", encrypt)
    white_button(root, "Decrypt", decrypt)
    white_button(root, "Back", lambda: show_classical_menu(root, back_func), pady=10)
# ------------------------------- Vernam Page -------------------------------
def show_vernam_page(root, back_func):
    clear_window(root)
    page_title(root, "Vernam Cipher")

    input_label(root, "Enter Text")
    text_entry = tk.Entry(root, width=40)
    text_entry.pack(pady=5)

    input_label(root, "Enter Key (same length as text)")
    key_entry = tk.Entry(root, width=40)
    key_entry.pack(pady=5)

    result_label = tk.Label(root, text="Result:", bg=BG_COLOR, fg=TEXT_COLOR)
    result_label.pack(pady=10)

    def process():
        text = text_entry.get()
        key = key_entry.get()

        if not validate_vernam_key(text, key):
            messagebox.showerror("Error", "Key must be letters only and same length as text")
            return

        result_label.config(text="Result: " + vernam(text, key))

    white_button(root, "Encrypt / Decrypt", process)
    white_button(root, "Back", lambda: show_classical_menu(root, back_func), pady=10)