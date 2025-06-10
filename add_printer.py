import tkinter as tk
from tkinter import messagebox
import subprocess
import tkinter.messagebox as messagebox

PRINT_SERVER = r"\\INSERT PRINT SERVER"

CREATE_NO_WINDOW = 0x08000000

def get_printers():
    server_name = PRINT_SERVER.strip("\\")
    # PS entry to find & list all printers on server
    ps_command = (
        f'Get-Printer -ComputerName {server_name} | '
        'Where-Object { $_.Shared -eq $true } | Select-Object -ExpandProperty Name'
    )
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            check=True,
            creationflags=CREATE_NO_WINDOW 
        )
        # Printer list determined by each line in PS command output
        printers = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return printers
    # Error handling on getting printer list
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to retrieve printers from server.\n{e}")
        return []

def install_printer(printer_name):
    full_printer_path = f"{PRINT_SERVER}\\{printer_name}"
    # PS command for installation
    cmd = [
        "rundll32",
        "printui.dll,PrintUIEntry",
        "/in", # Tells it to install printer
        "/n", # Mapping to path (next arg)
        full_printer_path
    ]
    try:
        subprocess.run(cmd, check=True, shell=True)
        messagebox.showinfo("Success", f"Printer '{printer_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to install printer '{printer_name}'.\nError: {e}")

def main():
    root = tk.Tk()
    root.title("Printer Installer")

    tk.Label(root, text=f"Printers on {PRINT_SERVER}").pack(pady=10)

    # Select which printer(s) to install
    lb = tk.Listbox(root, height=20, width=50, selectmode=tk.MULTIPLE)
    lb.pack(padx=20, pady=10)

    # Calls get_printers for dynamic list
    printers = get_printers()
    if not printers:
        printers = ["No printers found."]

    # Populates the list in dialog widget
    for printer in printers:
        lb.insert(tk.END, printer)

    def on_install():
        selected_indices = lb.curselection()
        if not selected_indices or printers[0].startswith("No printers"):
            messagebox.showwarning("No selection", "Please select valid printers to install.")
            return

        selected_printers = [lb.get(i) for i in selected_indices]

        for printer in selected_printers:
            install_printer(printer)

        messagebox.showinfo("Success", f"Installed {len(selected_printers)} printer(s).")

    install_btn = tk.Button(root, text="Install", command=on_install)
    install_btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

    
