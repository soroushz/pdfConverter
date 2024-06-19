# Step 1: Packages
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfReader
import os
import time

# Step 4: Custom File Dialog
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files",
                                                                               "*.*")])
    if file_path:
        selected_file.set(file_path)

# Step 5: Create drag and drop function
def drop(event):
    file_path = event.data
    # Remove curly braces if they exist
    if file_path.startswith("{") and file_path.endswith("}"):
        file_path = file_path[1:-1]
    selected_file.set(file_path)

# Step 7: PDF Conversion, Progress Bar, Error Handling
def start_conversion():
    try:
        pdf_path = selected_file.get()
        if not pdf_path:
            messagebox.showerror("Error", "No PDF file selected")
            return

        if not output_file.get():
            raise ValueError("Output file name cannot be empty")

        output_dir_path = output_dir.get()
        if not output_dir_path:
            messagebox.showerror("Error", "No output directory selected")
            return

        progress['value'] = 0
        root.update_idletasks()

        output_path = os.path.join(output_dir_path, f"{output_file.get()}.txt")

        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            total_pages = len(reader.pages)

            with open(output_path, "w", encoding="utf-8") as text_file:
                for i, page in enumerate(reader.pages):
                    progress['value'] = ((i + 1) / total_pages) * 100
                    root.update_idletasks()
                    time.sleep(0.5)  # Simulate conversion process

                    text = page.extract_text()
                    if text:
                        text_file.write(f"Page {i + 1}\n{'=' * 20}\n")
                        text_file.write(text)
                        text_file.write("\n\n")

        messagebox.showinfo("Success", "File converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Step 6: select new file directory
def choose_directory():
    directory = filedialog.askdirectory()
    output_dir.set(directory)

# Step 2: Create main window
root = TkinterDnD.Tk()
root.title("Enhanced PDF Converter")

# Step 5: register drag and drop
# Drag and Drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Step 7: Progress bar
progress = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress.pack()


# Step 3: Create widgets
# Output Options
output_dir = tk.StringVar()
output_file = tk.StringVar()
selected_file = tk.StringVar()

tk.Label(root, text="Output Directory:").pack()
tk.Entry(root, textvariable=output_dir).pack()
tk.Button(root, text="Browse", command=choose_directory).pack()

tk.Label(root, text="Output File Name:").pack()
tk.Entry(root, textvariable=output_file).pack()

tk.Label(root, text="Selected PDF File:").pack()
tk.Entry(root, textvariable=selected_file, state="readonly").pack()

open_button = tk.Button(root, text="Open PDF", command=open_file)
open_button.pack()

convert_button = tk.Button(root, text="Convert", command=start_conversion)
convert_button.pack()

root.mainloop()
