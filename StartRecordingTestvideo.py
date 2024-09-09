import os
import json
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pyttsx3
import sys

# Function to load selected camera from JSON file
def load_selected_camera():
    try:
        with open('selected_cameras.json', 'r') as file:
            cameras = json.load(file)
            if len(cameras) == 0:
                messagebox.showerror("Error", "No camera selected in the JSON file.")
                return None
            elif len(cameras) > 1:
                messagebox.showerror("Error", "Multiple cameras selected. Please select only one camera.")
                return None
            return cameras[0]  # Return the only selected camera
    except FileNotFoundError:
        messagebox.showerror("Error", "Selected cameras file not found.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error parsing the selected cameras file.")
        return None

# Function to load selected labels
def load_selected_labels():
    try:
        with open('label_data.json', 'r') as file:
            label_data = json.load(file)
            selected_labels = [row[4] for row in label_data if row[-1]]  # Use Gaze Direction if Use is True
            return selected_labels
    except FileNotFoundError:
        messagebox.showerror("Error", "Label data file not found.")
        return []

# Function to load settings from SettingsAnnotateAndPrepare.py
def load_settings():
    try:
        with open('compare_settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "Settings file not found.")
        return {}

# Function to center the window on the screen
def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Function to start the recording process
def start_recording():
    start_button.config(state=tk.DISABLED)  # Disable the start button after clicking

    # Load the selected camera from the JSON file
    selected_camera = load_selected_camera()

    if not selected_camera:
        return  # If no camera is correctly loaded, stop execution
    
    video_path = selected_camera['video_path']
    audio_path = selected_camera['audio_path']

    # Load labels and settings
    selected_labels = load_selected_labels()
    settings = load_settings()

    if not selected_labels:
        messagebox.showerror("Error", "No labels selected.")
        return

    num_sentences = int(settings.get("num_sentences", 2))
    interval_seconds = int(settings.get("interval_seconds", 5))
    extra_time_seconds = 5  # Extra time to keep the camera running after the last sentence
    
    # Get path and name from settings
    output_path = settings.get("path", "")
    base_name = settings.get("name", "output")
    
    # Ensure the path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    duration = num_sentences * interval_seconds + extra_time_seconds

    # Initialize speech engine
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 80)
    
    output_file = os.path.join(output_path, f"{base_name}_{selected_camera['name']}.mp4")

    # Construct the FFmpeg command for this camera
    ffmpeg_command = (
        f'ffmpeg -y -f dshow -i video="{video_path}" '
        f'-f dshow -i audio="{audio_path}" '
        f'-t {duration} -c:v libx264 -c:a aac -strict experimental "{output_file}"'
    )

    # Start FFmpeg process in the background
    process = subprocess.Popen(ffmpeg_command, shell=True)

    # Update the label with progress information
    for i in range(1, num_sentences + 1):
        direction = random.choice(selected_labels)
        engine.say(f"Please look {direction.replace('_', ' ')}")
        engine.runAndWait()
        progress_label.config(text=f"Sentences: {i}/{num_sentences}")
        root.update_idletasks()  # Ensure the label is updated
        time.sleep(interval_seconds)
    
    # Keep the camera running for an additional 5 seconds after the last sentence
    time.sleep(extra_time_seconds)

    # Wait for FFmpeg process to complete
    process.wait()

    messagebox.showinfo("Info", "Recording completed for the selected camera.")
    start_button.config(state=tk.NORMAL)  # Re-enable the start button after recording

# Initialize the main window
root = tk.Tk()
root.title("Start Recording")

# Set up GUI
progress_label = ttk.Label(root, text="Sentences: 0/0")
progress_label.pack(pady=10)

start_button = ttk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(expand=True, padx=20, pady=20)

# Center the window on the screen
root.update_idletasks()  # Update "requested size" from geometry manager
center_window(root)

# Run the main event loop
root.mainloop()
