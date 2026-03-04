import tkinter as tk
from tkinter import font as tkfont
import calendar

def validate_cnp(raw):
    cnp = raw.strip()

    if cnp == "":
        return False, "Invalid CNP: the field cannot be empty."
    
    if not cnp.isdigit():
        return False, "Invalid CNP: must contain digits only (no letters, spaces or special characters)."
    
    if len(cnp) != 13:
        return False, f"Invalid CNP: length must be exactly 13 digits (you entered {len(cnp)})."

    s  = int(cnp[0])
    aa = int(cnp[1:3])
    ll = int(cnp[3:5])
    zz = int(cnp[5:7])

    if s < 1 or s > 9:
        return False, "Invalid CNP: first digit (sex) must be between 1 and 9."
    
    month = int(ll)
    day   = int(zz)
    year  = 1900 + int(aa) if s in (1, 2) else 2000 + int(aa)

    if month < 1 or month > 12:
        return False, "Invalid CNP: birth month is invalid (must be between 01 and 12)."

    max_day = calendar.monthrange(year, month)[1]
    if day < 1 or day > max_day:
        return False, f"Invalid CNP: birth day ({day}) is not valid for month {month:02d}/{year}."

    WEIGHTS = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    jj = cnp[7:9]
    c  = int(cnp[12])

    total = sum(int(cnp[i]) * WEIGHTS[i] for i in range(12))
    remainder = total % 11
    expected = 1 if remainder == 10 else remainder

    if c != expected:
        return False, f"Invalid CNP: control digit is incorrect (expected: {expected}, found: {c})."

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
