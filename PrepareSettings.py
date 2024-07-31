import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sys

# Get the main window's position and size from the command line arguments
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])

# Function to center a window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.8, height_percentage=0.8):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Function to show a centered message box
def show_centered_messagebox(title, message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2)
    y = (screen_height // 2)
    root.geometry(f'+{x}+{y}')
    messagebox.showinfo(title, message)
    root.destroy()

# Function to save settings to a JSON file
def save_settings():
    settings = {
        "extraction_frequency": extraction_frequency_var.get(),
        "base_path": base_path_var.get(),
        "prepare_name": prepare_name_var.get(),
        "test_percentage": test_percentage_var.get(),
        "val_percentage": val_percentage_var.get()
    }

    with open('prepare_settings.json', 'w') as file:
        json.dump(settings, file)
    
    show_centered_messagebox("Info", "Settings saved successfully")

# Function to load settings from a JSON file
def retrieve_settings(show_message=True):
    try:
        with open('prepare_settings.json', 'r') as file:
            settings = json.load(file)
        
        extraction_frequency_var.set(settings.get("extraction_frequency", 1))
        base_path_var.set(settings.get("base_path", ""))
        prepare_name_var.set(settings.get("prepare_name", ""))
        test_percentage_var.set(settings.get("test_percentage", 0))
        val_percentage_var.set(settings.get("val_percentage", 0))
        if show_message:
            show_centered_messagebox("Info", "Settings retrieved successfully")
    except FileNotFoundError:
        show_centered_messagebox("Warning", "No saved settings found")
        return None

# Function to initialize the GUI with loaded settings
def initialize_settings():
    settings = retrieve_settings(show_message=False)
    if settings:
        extraction_frequency_var.set(settings.get("extraction_frequency", 1))
        base_path_var.set(settings.get("base_path", ""))
        prepare_name_var.set(settings.get("prepare_name", ""))
        test_percentage_var.set(settings.get("test_percentage", 0))
        val_percentage_var.set(settings.get("val_percentage", 0))

# Function to select a directory
def select_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        base_path_var.set(selected_directory)

# Initialize the main window
root = tk.Tk()
root.title("Prepare Data Settings")

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Create variables for the entry fields
extraction_frequency_var = tk.IntVar(value=1)
base_path_var = tk.StringVar()
prepare_name_var = tk.StringVar()
test_percentage_var = tk.IntVar(value=0)
val_percentage_var = tk.IntVar(value=0)

# Create and grid the labels and entry fields
ttk.Label(root, text="Extraction Frequency").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=extraction_frequency_var, width=20).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="(Extract every nth frame)").grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Path").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
path_frame = ttk.Frame(root)
path_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
ttk.Entry(path_frame, textvariable=base_path_var, state='readonly', width=50).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Button(path_frame, text="Browse", command=select_directory).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Name Prepare").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=prepare_name_var, width=50).grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Percentage to Copy to Test").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=test_percentage_var, width=20).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

ttk.Label(root, text="Percentage to Copy to Val").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
ttk.Entry(root, textvariable=val_percentage_var, width=20).grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

# Add Save and Retrieve buttons
save_button = ttk.Button(root, text="Save Settings", command=save_settings)
save_button.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

retrieve_button = ttk.Button(root, text="Retrieve Settings", command=lambda: retrieve_settings(show_message=True))
retrieve_button.grid(row=5, column=1, padx=10, pady=10, sticky=tk.E)

# Load settings when the application starts
initialize_settings()

# Run the main event loop
root.mainloop()
