import tkinter as tk
from tkinter import font as tkfont
import calendar

COUNTIES = {
        "01":"Alba","02":"Arad","03":"Arges","04":"Bacau","05":"Bihor",
        "06":"Bistrita-Nasaud","07":"Botosani","08":"Brasov","09":"Braila",
        "10":"Buzau","11":"Caras-Severin","12":"Cluj","13":"Constanta",
        "14":"Covasna","15":"Dambovita","16":"Dolj","17":"Galati","18":"Gorj",
        "19":"Harghita","20":"Hunedoara","21":"Ialomita","22":"Iasi","23":"Ilfov",
        "24":"Maramures","25":"Mehedinti","26":"Mures","27":"Neamt","28":"Olt",
        "29":"Prahova","30":"Satu Mare","31":"Salaj","32":"Sibiu","33":"Suceava",
        "34":"Teleorman","35":"Timis","36":"Tulcea","37":"Vaslui","38":"Valcea",
        "39":"Vrancea","40":"Bucharest","41":"Bucharest S1","42":"Bucharest S2",
        "43":"Bucharest S3","44":"Bucharest S4","45":"Bucharest S5","46":"Bucharest S6",
        "51":"Calarasi","52":"Giurgiu"
    }

WEIGHTS = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]

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
    jj = cnp[7:9]
    c  = int(cnp[12])

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

    if jj not in COUNTIES:
        return False, f"CNP invalid: codul județului ({jj}) nu este valid.", None
    total = sum(int(cnp[i]) * WEIGHTS[i] for i in range(12))
    remainder = total % 11
    expected = 1 if remainder == 10 else remainder

    if c != expected:
        return False, f"Invalid CNP: control digit is incorrect (expected: {expected}, found: {c})."

    return True, "Length validation passed."

def on_verify():
    raw = entry.get()
    valid, message = validate_cnp(raw)
    result_label.config(text=message)

    display = raw.strip() if raw.strip() else "(empty)"
    history.insert(0, (display, valid))
    if len(history) > 8:
        history.pop()

    for w in history_frame.winfo_children():
        w.destroy()
    for cnp_item, v in history:
        tk.Label(history_frame,
                 text=f"{'✔' if v else '✖'}  {cnp_item}",
                 fg="green" if v else "red",
                 font=("Courier New", 9)).pack(anchor="w")
root = tk.Tk()
root.title("CNP Validator")

entry = tk.Entry(root, font=("Courier New", 14), width=20)
entry.pack(padx=20, pady=10)

tk.Button(root, text="Validate", command=on_verify).pack(pady=5)

result_label = tk.Label(root, text="", font=("Segoe UI", 10), wraplength=300)
result_label.pack(padx=20, pady=10)

history_frame = tk.Frame(root)
history_frame.pack(padx=20, pady=5, fill="x")

history = []

root.mainloop()
