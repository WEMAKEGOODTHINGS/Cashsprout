from bank_system import BankSystem
import tkinter as tk
from tkinter import ttk, messagebox
import time

bank = BankSystem()

# ---------- UI Settings ----------
BG = "#0A0F24"
BTN = "#00E7FF"
FONT = ("Segoe UI", 12)

# ---------- Placeholder Entry ----------
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master, placeholder, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert(0, placeholder)
        self.config(fg="grey")
        self.bind("<FocusIn>", self.f_in)
        self.bind("<FocusOut>", self.f_out)

    def f_in(self, *_):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg="white")

    def f_out(self, *_):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg="grey")

# ---------- Neon Button ----------
def neon_button(master, text, cmd):
    return tk.Button(master, text=text, command=cmd, font=("Segoe UI", 11, "bold"),
                     fg=BG, bg=BTN, activebackground="#04D4F0", bd=0,
                     relief="flat", padx=15, pady=10, cursor="hand2",
                     highlightthickness=0)

# ---------- Splash Screen ----------
def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("400x250+500+250")
    splash.config(bg=BG)
    tk.Label(splash, text="BANKING SYSTEM", fg=BTN, bg=BG,
             font=("Segoe UI", 20, "bold")).pack(pady=30)
    tk.Label(splash, text="Loading...", fg="white", bg=BG,
             font=("Segoe UI", 10)).pack()
    prog = ttk.Progressbar(splash, orient="horizontal", length=250, mode="determinate")
    prog.pack(pady=20)
    for i in range(100):
        prog['value'] = i
        splash.update_idletasks()
        time.sleep(0.01)
    splash.destroy()
    login_window()

# ---------- Login Window ----------
def login_window():
    root = tk.Tk()
    root.title("Login")
    root.geometry("400x400")
    root.config(bg=BG)

    tk.Label(root, text="LOGIN", fg=BTN, bg=BG, font=("Segoe UI", 20, "bold")).pack(pady=20)
    username = EntryWithPlaceholder(root, "Enter Username", font=FONT, bg="#1A1F40", fg="white", insertbackground="white")
    username.pack(pady=8, ipadx=10, ipady=5)
    pin = EntryWithPlaceholder(root, "Enter PIN (4 digits)", font=FONT, bg="#1A1F40", fg="white", insertbackground="white")
    pin.pack(pady=8, ipadx=10, ipady=5)

    def login():
        u = username.get().strip()
        p = pin.get().strip()
        acc = bank.authenticate(u, p)
        if acc:
            root.destroy()
            dashboard(acc)
        else:
            messagebox.showerror("Error", "Invalid Username or PIN")

    neon_button(root, "LOGIN", login).pack(pady=15)
    neon_button(root, "Create New Account", lambda:(root.destroy(), create_account_ui())).pack()
    root.mainloop()

# ---------- Create Account UI ----------
def create_account_ui():
    win = tk.Tk()
    win.title("Create Account")
    win.geometry("420x520")
    win.config(bg=BG)

    tk.Label(win, text="Create Account", fg=BTN, bg=BG, font=("Segoe UI", 20, "bold")).pack(pady=10)
    tk.Label(win, text="Username ≥ 4 chars, no spaces\nPIN = 4 digits\nDeposit > 0",
             fg="yellow", bg=BG, font=("Segoe UI", 9, "italic")).pack(pady=5)

    acc = EntryWithPlaceholder(win, "Account Number", font=FONT, bg="#1A1F40", fg="white")
    name = EntryWithPlaceholder(win, "Full Name", font=FONT, bg="#1A1F40", fg="white")
    user = EntryWithPlaceholder(win, "Username", font=FONT, bg="#1A1F40", fg="white")
    pin = EntryWithPlaceholder(win, "PIN (4 digits)", font=FONT, bg="#1A1F40", fg="white")
    dep = EntryWithPlaceholder(win, "Initial Deposit", font=FONT, bg="#1A1F40", fg="white")

    for w in [acc, name, user, pin, dep]:
        w.pack(pady=8, ipadx=10, ipady=5)

    def create_acc():
        try:
            a = int(acc.get())
            if a <= 0:
                messagebox.showerror("Error", "Account number must be positive")
                return
            n = name.get().strip()
            u = user.get().strip()
            p = pin.get().strip()
            d = float(dep.get())
            if len(u) < 4 or " " in u:
                messagebox.showerror("Invalid Username", "Username must be ≥4 chars & no spaces")
                return
            if not p.isdigit() or len(p) != 4:
                messagebox.showerror("Invalid PIN", "PIN must be 4 digits")
                return
            if d <= 0:
                messagebox.showerror("Error", "Deposit must be > 0")
                return
            ok, msg = bank.create_account(a, n, u, p, d)
            messagebox.showinfo("Result", msg)
            if ok:
                win.destroy()
                login_window()
        except:
            messagebox.showerror("Error", "Please enter valid info")

    neon_button(win, "Create Account", create_acc).pack(pady=10)
    neon_button(win, "Back", lambda:(win.destroy(), login_window())).pack()
    win.mainloop()

# ---------- Dashboard ----------
def dashboard(acc):
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("410x480")
    dash.config(bg=BG)

    tk.Label(dash, text=f"Welcome {acc}", fg=BTN, bg=BG,
             font=("Segoe UI", 18, "bold")).pack(pady=15)

    def check_balance():
        ok, bal = bank.get_balance(acc)
        if ok:
            messagebox.showinfo("Balance", f"₹ {bal}")
        else:
            messagebox.showerror("Error", "Unable to fetch balance")

    def deposit():
        amt = simple_input("Deposit Amount")
        if amt:
            try:
                amt = float(amt)
                if amt <= 0:
                    messagebox.showerror("Error", "Amount must be >0")
                    return
                ok, msg = bank.deposit(acc, amt)
                messagebox.showinfo("Info", msg)
            except:
                messagebox.showerror("Error", "Enter a valid number")

    def withdraw():
        amt = simple_input("Withdraw Amount")
        if amt:
            try:
                amt = float(amt)
                if amt <= 0:
                    messagebox.showerror("Error", "Amount must be >0")
                    return
                ok, msg = bank.withdraw(acc, amt)
                messagebox.showinfo("Info", msg)
            except:
                messagebox.showerror("Error", "Enter a valid number")

    def transactions():
        win = tk.Toplevel(dash)
        win.title("Transactions")
        win.geometry("450x300")
        tree = ttk.Treeview(win, columns=("ID","Type","Amt","Time"), show="headings")
        tree.pack(fill="both", expand=True)
        for c in ("ID","Type","Amt","Time"): tree.heading(c, text=c)
        for r in bank.get_transactions(acc): tree.insert("", "end", values=r)

    for t, cmd in [("Check Balance", check_balance),
                   ("Deposit Money", deposit),
                   ("Withdraw Money", withdraw),
                   ("View Transactions", transactions),
                   ("Logout", lambda:(dash.destroy(), login_window()))]:
        neon_button(dash, t, cmd).pack(pady=10)

    dash.mainloop()

# ---------- Simple Input Popup ----------
def simple_input(title):
    win = tk.Toplevel()
    win.geometry("300x150")
    tk.Label(win, text=title).pack(pady=5)
    e = tk.Entry(win, font=FONT)
    e.pack(pady=5)
    v={"x":None}
    def sub(): v["x"]=e.get(); win.destroy()
    ttk.Button(win,text="OK",command=sub).pack()
    win.wait_window()
    return v["x"]

# ---------- Run App ----------
if __name__ == "__main__":
    splash_screen()
