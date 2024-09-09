import cv2
import os
import time
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random
import sys

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


# Function to load settings from a JSON file
def load_settings():
    try:
        with open('recording_settings.json', 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        print("No saved settings found")
        return None

# Function to load labels from a JSON file
def load_labels():
    try:
        with open('label_data.json', 'r') as file:
            labels = json.load(file)
        return labels
    except FileNotFoundError:
        print("No saved labels found")
        return None

# Function to say a sentence
def say_sentence(sentence):
    if pyttsx3 is not None:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 80)
        engine.say(sentence)
        engine.runAndWait()
    else:
        print(f"pyttsx3 is not installed. Would say: {sentence}")

# Function to create the directory structure
def create_directory_structure(base_path, recording_name, labels, max_selections_per_label):
    recording_path = os.path.join(base_path, recording_name, "Recording")
    os.makedirs(recording_path, exist_ok=True)

    for label_data in labels:
        if label_data[-1]:  # Only create directories for labels that are marked for use
            label = label_data[0]
            label_path = os.path.join(recording_path, label)
            os.makedirs(label_path, exist_ok=True)
            for j in range(1, max_selections_per_label + 1):
                subfolder_name = str(j)
                subfolder_path = os.path.join(label_path, subfolder_name)
                os.makedirs(subfolder_path, exist_ok=True)

    return recording_path

# Function to load selected cameras from a JSON file
def load_selected_cameras():
    try:
        with open('selected_cameras.json', 'r') as file:
            selected_cameras_data = json.load(file)
        selected_indexes = [camera["index"] for camera in selected_cameras_data]
        return selected_indexes
    except FileNotFoundError:
        print("No saved selected cameras found")
        return []

# Function to initialize cameras
def initialize_cameras(cameras):
    captures = []
    for camera in cameras:
        cap = cv2.VideoCapture(camera)
        captures.append(cap)
    return captures

# Function to stop the recording
def stop_recording():
    global running
    running = False
    if min(label_counts.values()) >= max_selections_per_label:
        return
    messagebox.showinfo("Info", "Recording stopped by user")

# Function to select label and prepare for recording
def select_label_and_prepare_recording():
    global current_save_path, label_counts
    available_labels = [label for label in label_counts if label_counts[label] < max_selections_per_label]
    selected_label = random.choice(available_labels)  # Randomly select a label
    label_counts[selected_label] += 1
    update_label_counts()
    say_sentence(f"Please look at {selected_label.replace('_', ' ')}")
    time.sleep(wait_seconds)  # Use the wait_seconds value from settings
    say_sentence("Start")
    
    subfolder = (label_counts[selected_label] - 1) % max_selections_per_label + 1
    current_save_path = [os.path.join(recording_path, selected_label, str(subfolder)) for _ in captures]

# Function to update the label counts in the GUI
def update_label_counts():
    global label_list
    label_list.set([f"{label}: {label_counts[label]}/{max_selections_per_label}" for label in label_counts])

# Function to handle window close event
def on_closing():
    stop_recording()
    root.destroy()

# Function to start the recording process
def start_recording():
    global running, start_time, current_save_path, out_writers
    running = True
    out_writers = [None] * len(captures)  # Initialize out_writers
    start_button.config(state=tk.DISABLED)  # Disable the start button after recording starts
    while running:
        if all(count >= max_selections_per_label for count in label_counts.values()):
            # Wait for the last recording to complete before ending
            time.sleep(recording_duration)  # Ensure the last recording lasts the full duration
            break
            
        if current_save_path[0] is None or time.time() - start_time >= recording_duration:
            select_label_and_prepare_recording()
            start_time = time.time()

            for i, out in enumerate(out_writers):
                if out is not None:
                    out.release()
                    
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            for i, cap in enumerate(captures):
                out_writers[i] = cv2.VideoWriter(os.path.join(current_save_path[i], f'camera_{selected_cameras[i]}.avi'), fourcc, 20.0, (640, 480))
            
        # Record video
        for i, cap in enumerate(captures):
            ret, frame = cap.read()
            if ret:
                out_writers[i].write(frame)

        # Check if recording duration has been reached
        if time.time() - start_time >= recording_duration:
            for out in out_writers:
                if out is not None:
                    out.release()
            current_save_path = [None] * len(captures)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Inform the user the recording is complete
    info_label.config(text="The recording is finished. You can close this window.")
    messagebox.showinfo("Recording Finished", "The recording is finished. You can close this window.")

    # Release all resources after message box is closed
    for out in out_writers:
        if out is not None:
            out.release()
    for cap in captures:
        cap.release()
    cv2.destroyAllWindows()

# Load settings, labels, and selected cameras
settings = load_settings()
labels = load_labels()
selected_cameras = load_selected_cameras()

if not settings or not labels:
    print("Settings or labels could not be loaded. Exiting...")
    exit(1)

# Ensure all required settings are present
required_settings = ["recording_duration", "base_path", "recording_name", "max_selections_per_label", "wait_seconds"]
for setting in required_settings:
    if setting not in settings:
        print(f"Missing setting: {setting}")
        exit(1)

recording_duration = int(settings["recording_duration"])
base_path = settings["base_path"]
recording_name = settings["recording_name"]
max_selections_per_label = int(settings["max_selections_per_label"])
wait_seconds = int(settings["wait_seconds"])

# Initialize the main window
root = tk.Tk()
root.title("Recording Control")

# Function to center the window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.3, height_percentage=0.5):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Center the window relative to the main window
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])
center_window(root, main_x, main_y, main_width, main_height)

# Change cursor to watch during loading
root.config(cursor="watch")

# Add a loading indicator (zandloper)
loading_label = ttk.Label(root, text="Loading, please wait...", font=('Helvetica', 16))
loading_label.grid(row=0, column=0, padx=20, pady=20)

root.update()

# Initialize cameras in a separate thread to keep the GUI responsive
def init_cameras_and_update_ui():
    global captures, out_writers, label_counts, current_save_path, recording_path, label_list, info_label, start_button
    captures = initialize_cameras(selected_cameras)
    
    # Remove the loading indicator
    loading_label.grid_remove()

    # Reset cursor to normal after loading
    root.config(cursor="")
    
    # Add the main UI elements after initialization
    label_counts = {label[0]: 0 for label in labels if label[-1]}
    recording_path = create_directory_structure(base_path, recording_name, labels, max_selections_per_label)
    current_save_path = [None] * len(captures)
    start_time = None
    
    # Add a frame for the label counts
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=20, pady=20)

    # Create a listbox to display label counts
    label_list = tk.StringVar(value=[f"{label}: 0/{max_selections_per_label}" for label in label_counts])
    listbox = tk.Listbox(frame, listvariable=label_list, height=15)  # Increase height for more labels
    listbox.grid(row=0, column=0)

    # Add a label to inform the user
    info_label = ttk.Label(root, text="Press 'Start Recording' to begin.")
    info_label.grid(row=1, column=0, padx=20, pady=20)

    # Add a button to start recording
    start_button = ttk.Button(root, text="Start Recording", command=lambda: start_recording_thread())
    start_button.grid(row=2, column=0, padx=20, pady=20)

    root.update()

def start_recording_thread():
    # Start the recording in a separate thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()

# Start the camera initialization in a separate thread
init_thread = threading.Thread(target=init_cameras_and_update_ui)
init_thread.start()

# Run the main event loop
root.mainloop()
