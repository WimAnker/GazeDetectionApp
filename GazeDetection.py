import tkinter as tk
from tkinter import Menu
import subprocess
import sys
import platform

# Bepaal het juiste Python-commando op basis van het besturingssysteem
python_command = "python" if platform.system() == "Windows" else "python3"

# Function to run external scripts with the main window's position
def run_script(script_name, root):
    try:
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        p = subprocess.Popen([python_command, script_name, str(x), str(y), str(width), str(height)])
        subprocesses.append(p)
    except Exception as e:
        print(f"Failed to run {script_name}: {e}")

# Function placeholders
def collect_data_settings():
    run_script('RecordingSettings.py', root)

def collect_data_cameras_positioning():
    run_script('FindCameras.py', root)

def collect_data_start_recording_script():
    run_script('StartRecording.py', root)

def setup_labels():
    run_script('SetupLabels.py', root)

def model_training():
    run_script('ModelTraining.py', root)

def annotate_live_video():
    run_script('AnnotateLiveVideo.py', root)

def prepare_settings():
    run_script('PrepareSettings.py', root)

def prepare_data_for_training():
    run_script('PrepareDataset.py', root)

# Function to center the window
def center_window(root, width_percentage=0.5, height_percentage=0.5):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

# Function to handle window close event
def on_closing():
    for p in subprocesses:
        p.terminate()
    root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Application")

# Center and resize the window
center_window(root)

# Create a list to track subprocesses
subprocesses = []

# Create a menu bar
menu_bar = Menu(root)

# Create "Collect Data" submenu
collect_data_menu = Menu(menu_bar, tearoff=0)
collect_data_menu.add_command(label="Settings", command=collect_data_settings)
collect_data_menu.add_command(label="Setup Labels", command=setup_labels)
collect_data_menu.add_command(label="Cameras and Positioning", command=collect_data_cameras_positioning)
collect_data_menu.add_command(label="Start Recording Script", command=collect_data_start_recording_script)
menu_bar.add_cascade(label="Collect Data", menu=collect_data_menu)

# Create "Prepare Data" submenu
prepare_data_menu = Menu(menu_bar, tearoff=0)
prepare_data_menu.add_command(label="Settings for Prepare Data", command=prepare_settings)
prepare_data_menu.add_command(label="Prepare Data for Training", command=prepare_data_for_training)
menu_bar.add_cascade(label="Prepare Data", menu=prepare_data_menu)

# Add "Model Training" option to the menu bar
menu_bar.add_command(label="Model Training", command=model_training)

# Add "Annotate Live Video" option to the menu bar
menu_bar.add_command(label="Annotate Live Video", command=annotate_live_video)

# Add the menu bar to the root window
root.config(menu=menu_bar)

# Set the protocol for handling window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
root.mainloop()
