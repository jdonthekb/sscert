import tkinter as tk
import os
import sys
import ctypes
from tkinter import simpledialog
from subprocess import Popen, PIPE

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

def log_exception(exception_message):
    log_file_path = os.path.join(get_script_dir(), "error_log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(exception_message + "\n")

def generate_and_export_cert():
    if not run_as_admin():
        return

    try:
        friendly_name = friendly_name_entry.get()
        password = simpledialog.askstring("Password", "Enter a password for the certificate:", show='*')
        if not password:
            return

        script_dir = get_script_dir()
        export_path = os.path.join(script_dir, f"{friendly_name}.pfx")
        
        command = rf"""
        $cert = New-SelfSignedCertificate -certstorelocation cert:\localmachine\my -dnsname localhost -FriendlyName '{friendly_name}' -Subject '{friendly_name}' -Type CodeSigningCert;
        $pwd = ConvertTo-SecureString -String '{password}' -Force -AsPlainText;
        $path = 'cert:\localMachine\my\' + $cert.thumbprint;
        Export-PfxCertificate -cert $path -FilePath '{export_path}' -Password $pwd;
        """
        
        process = Popen(["powershell", "-Command", command], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        if error:
            log_exception(error.decode('utf-8'))
            result_label.config(text="Error occurred. Check the log file for details.")
        else:
            result_label.config(text=f"Certificate exported to {export_path}")
    except Exception as e:
        log_exception(str(e))

appVersion = "v1.1"
root = tk.Tk()
root.title("SSCert" + " " + appVersion + " by " + "Josh Dwight" )
root.geometry("400x100")

tk.Label(root, text="Friendly Name:").pack()
friendly_name_entry = tk.Entry(root, width=40)
friendly_name_entry.pack()

generate_button = tk.Button(root, text="Generate and Export Cert", command=generate_and_export_cert)
generate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
