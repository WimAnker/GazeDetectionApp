import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys

# Function to save settings to a JSON file
def save_settings():
    settings = {
        "num_sentences": num_sentences_entry.get(),
        "interval_seconds": interval_seconds_entry.get(),
        "path": path_entry.get(),
        "name": name_entry.get()
    }
    with open("compare_settings.json", "w") as json_file:
        json.dump(settings, json_file)
    messagebox.showinfo("Info", "Settings saved successfully.")

# Function to retrieve settings from a JSON file
def retrieve_settings():
    if os.path.exists("compare_settings.json"):
        with open("compare_settings.json", "r") as json_file:
            settings = json.load(json_file)
            num_sentences_entry.delete(0, tk.END)
            num_sentences_entry.insert(0, settings["num_sentences"])
            interval_seconds_entry.delete(0, tk.END)
            interval_seconds_entry.insert(0, settings["interval_seconds"])
            path_entry.delete(0, tk.END)
            path_entry.insert(0, settings["path"])
            name_entry.delete(0, tk.END)
            name_entry.insert(0, settings["name"])
        messagebox.showinfo("Info", "Settings retrieved successfully.")
    else:
        messagebox.showerror("Error", "Settings file not found.")

# Function to load settings automatically on startup
def load_settings_on_startup():
    if os.path.exists("compare_settings.json"):
        with open("compare_settings.json", "r") as json_file:
            settings = json.load(json_file)
            num_sentences_entry.delete(0, tk.END)
            num_sentences_entry.insert(0, settings["num_sentences"])
            interval_seconds_entry.delete(0, tk.END)
            interval_seconds_entry.insert(0, settings["interval_seconds"])
            path_entry.delete(0, tk.END)
            path_entry.insert(0, settings["path"])
            name_entry.delete(0, tk.END)
            name_entry.insert(0, settings["name"])

# Function to browse for a directory
def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_directory)

# Initialize the main window
root = tk.Tk()
root.title("Recording Control")

# Check if the script received position and size parameters
if len(sys.argv) == 5:
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    main_width = int(sys.argv[3])
    main_height = int(sys.argv[4])
    
    # Calculate new size (e.g., 80% of the main window size)
    width = int(main_width * 0.8)
    height = int(main_height * 0.8)
    
    # Calculate new position to center the window within the main window
    new_x = x + (main_width - width) // 2
    new_y = y + (main_height - height) // 2
    
    # Set the new geometry of the window
    root.geometry(f'{width}x{height}+{new_x}+{new_y}')
else:
    # If no parameters are provided, center the window on the screen
    root.geometry('800x600')  # Default size
    root.eval('tk::PlaceWindow . center')

# Add parameters for number of sentences and interval
ttk.Label(root, text="Number of Sentences:").grid(row=0, column=0, padx=10, pady=5)
num_sentences_entry = ttk.Entry(root)
num_sentences_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Interval Between Sentences (seconds):").grid(row=1, column=0, padx=10, pady=5)
interval_seconds_entry = ttk.Entry(root)
interval_seconds_entry.grid(row=1, column=1, padx=10, pady=5)

# Add parameters for path and name of the video
ttk.Label(root, text="Save Path:").grid(row=2, column=0, padx=10, pady=5)
path_entry = ttk.Entry(root)
path_entry.grid(row=2, column=1, padx=10, pady=5)

browse_button = ttk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=2, column=2, padx=5, pady=5)

ttk.Label(root, text="Video Name:").grid(row=3, column=0, padx=10, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(row=3, column=1, padx=10, pady=5)

# Add buttons for Save Settings and Retrieve Settings
save_button = ttk.Button(root, text="Save Settings", command=save_settings)
save_button.grid(row=4, column=0, pady=10)

retrieve_button = ttk.Button(root, text="Retrieve Settings", command=retrieve_settings)
retrieve_button.grid(row=4, column=1, pady=10)

# Automatically load settings when the application starts
load_settings_on_startup()

# Run the main event loop
root.mainloop()
