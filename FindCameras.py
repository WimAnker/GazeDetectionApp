import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import json
import sys

# Get the main window's position and size from the command line arguments
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])

open_camera_windows = []

# Load the camera list from a JSON file
def load_camera_list_from_json(file_path):
    with open(file_path, 'r') as file:
        camera_list = json.load(file)
    return camera_list

# Step 1: Detect connected cameras using OpenCV
def detect_cameras():
    root.config(cursor="watch")
    root.update_idletasks()
    cameras = []
    
    for index in range(10):  # Limit to first 10 indexes to prevent infinite loop
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras.append(index)
        cap.release()
    
    root.config(cursor="")
    return cameras

# Function to save selected cameras to a JSON file
def save_selected_cameras():
    selected_cameras = []
    for camera in camera_vars:
        if camera[2].get():  # If the checkbox is selected
            selected_cameras.append({
                "index": camera[0], 
                "name": camera[1], 
                "video_path": camera[3], 
                "audio_path": camera[4]
            })
    
    if selected_cameras:
        with open('selected_cameras.json', 'w') as file:
            json.dump(selected_cameras, file, indent=4)
        messagebox.showinfo("Info", "Selected cameras saved successfully")
    else:
        messagebox.showwarning("Warning", "No cameras selected to save")

# Function to show live feed from a camera
def show_camera_feed(camera_index):
    root.config(cursor="watch")
    root.update_idletasks()
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        root.config(cursor="")
        messagebox.showerror("Error", f"Cannot open camera {camera_index}")
        return
    
    window_name = f"Camera {camera_index}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    open_camera_windows.append(window_name)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    if window_name in open_camera_windows:
        try:
            cv2.destroyWindow(window_name)
            open_camera_windows.remove(window_name)
        except cv2.error as e:
            print(f"Error closing window {window_name}: {e}")
    root.config(cursor="")

# Function to center the window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.5, height_percentage=0.5):
    width = int(main_width * width_percentage)
    height = int(main_height * height_percentage)
    x = main_x + (main_width - width) // 2
    y = main_y + (main_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the main window
root = tk.Tk()
root.title("Find Connected Cameras")

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Detect connected cameras
camera_indices = detect_cameras()

# Load the camera list from the JSON file
camera_list = load_camera_list_from_json('camera_list.json')

# Combine camera indices with their names and paths from the JSON file
combined_cameras = []
for i, index in enumerate(camera_indices):
    if i < len(camera_list):
        name = camera_list[i]["name"]
        video_path = camera_list[i]["video_path"]
        audio_path = camera_list[i]["audio_path"]
        combined_cameras.append((index, name, video_path, audio_path))
    else:
        combined_cameras.append((index, f"Camera {index}", None, None))

camera_vars = []

# Create and grid the labels, checkboxes, and test buttons
for index, (camera_index, camera_name, video_path, audio_path) in enumerate(combined_cameras):
    camera_var = tk.BooleanVar()
    ttk.Label(root, text=f"Camera {camera_index}: {camera_name}").grid(row=index, column=0, padx=10, pady=5, sticky=tk.W)
    ttk.Checkbutton(root, variable=camera_var).grid(row=index, column=1, padx=10, pady=5, sticky=tk.W)
    test_button = ttk.Button(root, text="Test", command=lambda c=camera_index: show_camera_feed(c))
    test_button.grid(row=index, column=2, padx=10, pady=5, sticky=tk.W)
    camera_vars.append((camera_index, camera_name, camera_var, video_path, audio_path))

# Add Save button
save_button = ttk.Button(root, text="Save Selected Cameras", command=save_selected_cameras)
save_button.grid(row=len(combined_cameras), column=0, columnspan=3, padx=10, pady=10)

# Function to handle window close event
def on_closing():
    root.config(cursor="watch")
    for window in open_camera_windows:
        try:
            if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow(window)
        except cv2.error as e:
            print(f"Error closing window {window}: {e}")
    open_camera_windows.clear()
    root.config(cursor="")
    root.destroy()

# Set the protocol for handling window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
root.mainloop()
