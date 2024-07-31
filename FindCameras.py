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

# Function to detect connected cameras
def detect_cameras():
    root.config(cursor="wait")
    root.update_idletasks()
    index = 0
    cameras = []
    while index < 10:  # Limit to first 10 indexes to prevent infinite loop
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras.append(index)
        cap.release()
        index += 1
    root.config(cursor="")
    return cameras

# Function to save selected cameras to a JSON file
def save_selected_cameras():
    selected_cameras = []
    for var in camera_vars:
        if var[1].get():
            selected_cameras.append(var[0])
    
    with open('selected_cameras.json', 'w') as file:
        json.dump(selected_cameras, file)
    
    messagebox.showinfo("Info", "Selected cameras saved successfully")

# Function to show live feed from a camera
def show_camera_feed(port):
    root.config(cursor="wait")
    root.update_idletasks()
    cap = cv2.VideoCapture(port)
    if not cap.isOpened():
        root.config(cursor="")
        messagebox.showerror("Error", f"Cannot open camera {port}")
        return
    
    window_name = f"Camera {port}"
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
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Initialize the main window
root = tk.Tk()
root.title("Find Connected Cameras")

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Detect connected cameras
connected_cameras = detect_cameras()
camera_vars = []

# Create and grid the labels, checkboxes, and test buttons
for index, camera in enumerate(connected_cameras):
    camera_var = tk.BooleanVar()
    ttk.Label(root, text=f"Positioneer Camera {index} (Port {camera})").grid(row=index, column=0, padx=10, pady=5, sticky=tk.W)
    ttk.Checkbutton(root, variable=camera_var).grid(row=index, column=1, padx=10, pady=5, sticky=tk.W)
    test_button = ttk.Button(root, text="Test", command=lambda c=camera: show_camera_feed(c))
    test_button.grid(row=index, column=2, padx=10, pady=5, sticky=tk.W)
    camera_vars.append((camera, camera_var))

# Add Save button
save_button = ttk.Button(root, text="Save Selected Cameras", command=save_selected_cameras)
save_button.grid(row=len(connected_cameras), column=0, columnspan=3, padx=10, pady=10)

# Function to handle window close event
def on_closing():
    root.config(cursor="wait")
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
