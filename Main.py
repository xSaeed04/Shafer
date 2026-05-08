import tkinter as tk
from Authentication import show_login_page

root = tk.Tk()

root.title("Shafer🔒")
root.geometry("500x500")

root.configure(bg="#1E1E2F")

show_login_page(root)
root.mainloop()