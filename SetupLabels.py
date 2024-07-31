import tkinter as tk
from tkinter import ttk, messagebox
import json
import sys

# Get the main window's position and size from the command line arguments
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])

# Function to save data to a JSON file
def save_data():
    data_to_save = []
    for row in rows:
        row_data = [entry.get() for entry in row[:-1]]
        row_data.append(row[-1].get())
        data_to_save.append(row_data)
    
    with open('label_data.json', 'w') as file:
        json.dump(data_to_save, file)
    
    messagebox.showinfo("Info", "Data saved successfully")

# Function to load data from a JSON file
def load_data():
    try:
        with open('label_data.json', 'r') as file:
            loaded_data = json.load(file)
        
        for i, row_data in enumerate(loaded_data):
            for j, value in enumerate(row_data):
                if j < len(row_data) - 1:
                    rows[i][j].delete(0, tk.END)
                    rows[i][j].insert(0, value)
                else:
                    rows[i][j].set(value)
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved data found")

# Function to center the window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.7, height_percentage=0.7):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the main window
root = tk.Tk()
root.title("Setup Labels")

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Create a frame for the table
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add column headers
columns = ["Label", "Label (NL)", "Label (EN)", "Gaze Direction", "Sentence", "Dutch Translation", "Use (Yes/No)"]
for col_num, header in enumerate(columns):
    ttk.Label(frame, text=header).grid(row=0, column=col_num, padx=5, pady=2)

# Add rows of data entries
rows = []
try:
    with open('label_data.json', 'r') as file:
        table_data = json.load(file)
except FileNotFoundError:
    table_data = [
        ["forward", "Vooruit", "Forward", "Forward", "Look forward.", "Kijk vooruit.", False],
        ["left", "Links", "Left", "Left", "Look to the left.", "Kijk naar links.", False],
        ["right", "Rechts", "Right", "Right", "Look to the right.", "Kijk naar rechts.", False],
        ["mirror_interior", "Binnenspiegel", "Interior Mirror", "Interior Mirror", "Look at the interior mirror.", "Kijk in de binnenspiegel.", False],
        ["mirror_right", "Rechter Buitenspiegel", "Right Side Mirror", "Right Side Mirror", "Look at the right side mirror.", "Kijk in de rechter zijspiegel.", False],
        ["mirror_left", "Linker Buitenspiegel", "Left Side Mirror", "Left Side Mirror", "Look at the left side mirror.", "Kijk in de linker zijspiegel.", False],
        ["shoulder_right", "Rechterschouder", "Right Shoulder", "Right Shoulder", "Look over your right shoulder.", "Kijk over je rechter schouder.", False],
        ["shoulder_left", "Linkerschouder", "Left Shoulder", "Left Shoulder", "Look over your left shoulder.", "Kijk over je linker schouder.", False],
        ["dashboard_straight_down", "Dashboard", "Dashboard", "Dashboard Straight Down", "Look straight down at the dashboard.", "Kijk recht naar beneden naar het dashboard.", False],
        ["dashboard_down_right", "Middenconsole", "Center Console", "Dashboard Down Towards Center Console", "Look down towards the center console.", "Kijk naar beneden naar de middenconsole.", False],
        ["forward_right", "Rechts vooruit", "Forward Right", "Forward Right", "Look forward and to the right.", "Kijk vooruit en naar rechts.", False],
        ["forward_left", "Links vooruit", "Forward Left", "Forward Left", "Look forward and to the left.", "Kijk vooruit en naar links.", False]
    ]

for row_num, row_data in enumerate(table_data):
    row_entries = []
    for col_num, value in enumerate(row_data[:-1]):
        entry = ttk.Entry(frame)
        entry.grid(row=row_num + 1, column=col_num, padx=5, pady=2)
        entry.insert(0, value)
        row_entries.append(entry)
    use_var = tk.BooleanVar(value=row_data[-1])
    checkbutton = ttk.Checkbutton(frame, variable=use_var)
    checkbutton.grid(row=row_num + 1, column=len(row_data) - 1, padx=5, pady=2)
    row_entries.append(use_var)
    rows.append(row_entries)

# Add Save and Load buttons
save_button = ttk.Button(root, text="Save Labels", command=save_data)
save_button.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

load_button = ttk.Button(root, text="Retreive Labels", command=load_data)
load_button.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)

# Load data when the application starts
load_data()

# Run the main event loop
root.mainloop()
