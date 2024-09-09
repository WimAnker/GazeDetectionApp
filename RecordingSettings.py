import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sys

# Get the main window's position and size from the command line arguments
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])

# Function to save settings to a JSON file
def save_settings():
    settings = {
        "recording_duration": recording_duration_var.get(),
        "base_path": base_path_var.get(),
        "recording_name": recording_name_var.get(),
        "max_selections_per_label": max_selections_per_label_var.get(),
        "wait_seconds": wait_seconds_var.get(),
        "resolution": resolution_var.get(),
        "framerate": framerate_var.get()
    }
    
    with open('recording_settings.json', 'w') as file:
        json.dump(settings, file)
    
    messagebox.showinfo("Info", "Settings saved successfully")

# Function to load settings from a JSON file
def load_settings():
    try:
        with open('recording_settings.json', 'r') as file:
            settings = json.load(file)
        
        recording_duration_var.set(settings["recording_duration"])
        base_path_var.set(settings["base_path"])
        recording_name_var.set(settings["recording_name"])
        max_selections_per_label_var.set(settings["max_selections_per_label"])
        wait_seconds_var.set(settings.get("wait_seconds", 2))  # Default to 2 seconds if not found
        resolution_var.set(settings.get("resolution", "640x480"))  # Default resolution
        framerate_var.set(settings.get("framerate", 20))  # Default framerate
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved settings found")
        return

# Function to select a directory
def select_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        base_path_var.set(selected_directory)

# Function to center the window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.4, height_percentage=0.5):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the main window
root = tk.Tk()
root.title("Settings")

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Create variables for the entry fields
recording_duration_var = tk.IntVar()
base_path_var = tk.StringVar()
recording_name_var = tk.StringVar()
max_selections_per_label_var = tk.StringVar()
wait_seconds_var = tk.IntVar()
resolution_var = tk.StringVar()
framerate_var = tk.IntVar()

# Load the settings when the application starts
load_settings()

# Create and grid the labels and entry fields
ttk.Label(root, text="Recording Duration").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=recording_duration_var, width=40).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Path").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
path_frame = ttk.Frame(root)
path_frame.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
ttk.Entry(path_frame, textvariable=base_path_var, state='readonly', width=40).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Button(path_frame, text="Browse", command=select_directory).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Name Recording").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=recording_name_var, width=40).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Max Selections per Label").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=max_selections_per_label_var, width=5).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Wait Seconds").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=wait_seconds_var, width=5).grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Resolution (e.g., 640x480)").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=resolution_var, width=40).grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Framerate (10-30)").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=framerate_var, width=5).grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

# Add Save and Load buttons
save_button = ttk.Button(root, text="Save Settings", command=save_settings)
save_button.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)

load_button = ttk.Button(root, text="Retrieve Settings", command=load_settings)
load_button.grid(row=7, column=1, padx=10, pady=10, sticky=tk.E)

# Run the main event loop
root.mainloop()
