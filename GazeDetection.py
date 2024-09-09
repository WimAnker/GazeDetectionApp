import tkinter as tk
from tkinter import Menu, messagebox
import subprocess
import platform
import json

# Determine the correct Python command based on the operating system
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
        p.wait()  # Wait for the script to finish
    except Exception as e:
        print(f"Failed to run {script_name}: {e}")

# Show a warning before running the camera positioning for test video creation
def show_testvideo_warning():
    warning_message = (
        "Warning: For creating a test video, you should only select one camera. "
        "Please ensure that only one camera is connected via the USB ports!"
    )
    messagebox.showinfo("Test Video Warning", warning_message)

# Function to validate that only one camera is selected
def validate_single_camera_selection():
    try:
        with open('selected_cameras.json', 'r') as file:
            selected_cameras = json.load(file)
        if len(selected_cameras) != 1:
            messagebox.showerror("Error", "You must select exactly one camera for creating a test video.")
            return False
        return True
    except FileNotFoundError:
        messagebox.showerror("Error", "No cameras were selected. Please run the camera selection process again.")
        return False

def collect_data_settings():
    run_script('RecordingSettings.py', root)

def collect_data_cameras_positioning():
    run_script('FindCameras.py', root)

def collect_data_start_recording_script():
    run_script('StartRecording.py', root)

def setup_labels():
    run_script('SetupLabels.py', root)

def start_recording_testvideo():
    run_script('StartRecordingTestvideo.py', root)

def settings_testvideo():
    run_script('SettingsTestvideo.py', root)

def create_testvideo_cameras_positioning():
    show_testvideo_warning()  # Show the warning for test video
    run_script('FindCameras.py', root)
    if not validate_single_camera_selection():
        return

def annotate_video():
    run_script('AnnotateVideo.py', root)

def compare_test_and_model_annotation():
    run_script('CompareTestAndModelAnnotation.py', root)

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
collect_data_menu.add_command(label="Settings Test Recording", command=collect_data_settings)
collect_data_menu.add_command(label="Setup Labels", command=setup_labels)
collect_data_menu.add_command(label="Cameras and Positioning", command=collect_data_cameras_positioning)
collect_data_menu.add_command(label="Start Recording Script", command=collect_data_start_recording_script)
menu_bar.add_cascade(label="Collect Data", menu=collect_data_menu)

# Create "Prepare Data" submenu
prepare_data_menu = Menu(menu_bar, tearoff=0)
prepare_data_menu.add_command(label="Settings for Prepare Data", command=prepare_settings)
prepare_data_menu.add_command(label="Prepare Data for Training", command=prepare_data_for_training)
menu_bar.add_cascade(label="Prepare Data", menu=prepare_data_menu)

# Create "Create Testvideo" submenu
create_testvideo_menu = Menu(menu_bar, tearoff=0)
create_testvideo_menu.add_command(label="Settings Testvideo", command=settings_testvideo)
create_testvideo_menu.add_command(label="Setup Labels", command=setup_labels)
create_testvideo_menu.add_command(label="Cameras and Positioning", command=create_testvideo_cameras_positioning)
create_testvideo_menu.add_command(label="Start Recording Testvideo", command=start_recording_testvideo)
menu_bar.add_cascade(label="Create Testvideo", menu=create_testvideo_menu)

# Add "Annotate Video" option to the menu bar
menu_bar.add_command(label="Annotate Video", command=annotate_video)

# Add "Compare Test- and Model Annotation" option to the menu bar
menu_bar.add_command(label="Compare Test- and Model Annotation", command=compare_test_and_model_annotation)

# Add the menu bar to the root window
root.config(menu=menu_bar)

# Set the protocol for handling window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
root.mainloop()
