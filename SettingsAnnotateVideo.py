import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys

# Functie om een modelbestand te selecteren (zoals het .pt modelbestand)
def browse_model():
    filename = filedialog.askopenfilename(title="Select YOLO Model (.pt)", filetypes=[("PyTorch Model", "*.pt")])
    if filename:
        model_entry.delete(0, tk.END)
        model_entry.insert(0, filename)

# Functie om de video te kiezen die geannoteerd moet worden
def browse_video():
    filename = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.m4v *.webm"),
            ("All Files", "*.*")
        ]
    )
    if filename:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, filename)

# Functie om de directory te kiezen waar de CSV wordt opgeslagen
def browse_output_directory():
    directory = filedialog.askdirectory(title="Select Output Directory")
    if directory:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, directory)

# Functie om instellingen op te slaan in een JSON-bestand
def save_settings():
    settings = {
        "model_path": model_entry.get(),
        "video_path": video_entry.get(),
        "output_dir": output_dir_entry.get(),
        "output_filename": output_file_entry.get()
    }
    with open("SettingsAnnotateVideo.json", "w") as outfile:
        json.dump(settings, outfile)
    messagebox.showinfo("Info", "Settings saved successfully.")

# Functie om instellingen op te halen uit een JSON-bestand
def retrieve_settings():
    if os.path.exists("SettingsAnnotateVideo.json"):
        with open("SettingsAnnotateVideo.json", "r") as infile:
            settings = json.load(infile)
            model_entry.delete(0, tk.END)
            model_entry.insert(0, settings.get("model_path", ""))
            video_entry.delete(0, tk.END)
            video_entry.insert(0, settings.get("video_path", ""))
            output_dir_entry.delete(0, tk.END)
            output_dir_entry.insert(0, settings.get("output_dir", ""))
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(0, settings.get("output_filename", ""))

# Functie om automatisch instellingen te laden bij opstarten
def load_settings_on_startup():
    if os.path.exists("SettingsAnnotateVideo.json"):
        retrieve_settings()

# Initialiseer het hoofdvenster
root = tk.Tk()
root.title("Settings Annotate Video")

# Check voor venstergrootte en -positie parameters
if len(sys.argv) == 5:
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    main_width = int(sys.argv[3])
    main_height = int(sys.argv[4])
    
    width = 1000  # Breedte aangepast aan de invoervelden
    height = 250  # Geschatte hoogte gebaseerd op het aantal invoervelden en knoppen
    new_x = x + (main_width - width) // 2
    new_y = y + (main_height - height) // 2
    root.geometry(f'{width}x{height}+{new_x}+{new_y}')
else:
    width = 1000
    height = 250
    root.geometry(f'{width}x{height}')
    root.eval('tk::PlaceWindow . center')

# Interface-elementen voor het modelbestand, video en uitvoermap met voldoende breedte
ttk.Label(root, text="YOLO Model Path (.pt):").grid(row=0, column=0, padx=10, pady=5)
model_entry = ttk.Entry(root, width=120)
model_entry.grid(row=0, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_model).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(root, text="Video File:").grid(row=1, column=0, padx=10, pady=5)
video_entry = ttk.Entry(root, width=120)
video_entry.grid(row=1, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_video).grid(row=1, column=2, padx=5, pady=5)

ttk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5)
output_dir_entry = ttk.Entry(root, width=120)
output_dir_entry.grid(row=2, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=browse_output_directory).grid(row=2, column=2, padx=5, pady=5)

ttk.Label(root, text="Output Filename:").grid(row=3, column=0, padx=10, pady=5)
output_file_entry = ttk.Entry(root, width=120)
output_file_entry.grid(row=3, column=1, padx=10, pady=5)

# Knoppen voor het opslaan en ophalen van instellingen
ttk.Button(root, text="Save Settings", command=save_settings).grid(row=4, column=0, pady=10)
ttk.Button(root, text="Retrieve Settings", command=retrieve_settings).grid(row=4, column=1, pady=10)

# Automatisch instellingen laden bij het starten
load_settings_on_startup()

# Start de mainloop
root.mainloop()
