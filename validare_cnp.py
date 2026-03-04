import tkinter as tk
from tkinter import font as tkfont

def validate_cnp(raw):
    cnp = raw.strip()

    if cnp == "":
        return False, "Invalid CNP: the field cannot be empty."
    
    if len(cnp) != 13:
        return False, f"Invalid CNP: length must be exactly 13 digits (you entered {len(cnp)})."

    return True, "Length validation passed."

def on_verify():
    valid, message = validate_cnp(entry.get())
    result_label.config(text=message)

root = tk.Tk()
root.title("CNP Validator")

entry = tk.Entry(root, font=("Courier New", 14), width=20)
entry.pack(padx=20, pady=10)

tk.Button(root, text="Validate", command=on_verify).pack(pady=5)

result_label = tk.Label(root, text="", font=("Segoe UI", 10), wraplength=300)
result_label.pack(padx=20, pady=10)

root.mainloop()
