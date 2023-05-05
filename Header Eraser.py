import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime


def select_directory():
    global directory
    directory = filedialog.askdirectory()


def read_files():
    try:
        log_text.delete("1.0", "end")
        log_file_path = os.path.join(directory, "logs", "log.txt")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "a") as log_file:
            log_file.write(f"\n\n\n{datetime.datetime.now()}\n")
            for file in os.listdir(directory):
                f = os.path.join(directory, file)
                if os.path.isfile(f):
                    with open(f, 'rb') as f:
                        b = f.read()
                        i = 0
                        while i < len(b):
                            if b[i:i+7] == b'UnityFS':
                                c = b[i:]
                                break
                            i += 1
                        if i == len(b):
                            log_text.insert("end", f"UnityFS not found in file {file}\n")
                            log_file.write(f"{file}, UnityFS not found\n")
                        else:
                            output_file_path = os.path.join(directory, "Read", file+'.read')
                            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                            with open(output_file_path, "wb") as output_file:
                                output_file.write(c)
                            log_text.insert("end", f"{file} read successfully\n")
                            log_file.write(f"{file}, Success\n")
        messagebox.showinfo("Success", "All files have been processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


window = tk.Tk()
window.title("UnityFS Reader")

select_dir_button = tk.Button(window, text="Select Directory", command=select_directory)
select_dir_button.pack(pady=10)

read_files_button = tk.Button(window, text="Read Files", command=read_files)
read_files_button.pack(pady=10)

log_text = tk.Text(window, height=10, width=50)
log_text.pack(pady=10)

window.mainloop()
