import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import platform

open_camera_windows = []

# Function to detect connected cameras
def detect_cameras():
    root.config(cursor="watch")  # Show busy cursor
    root.update_idletasks()
    cameras = []

    # Detecteer het huidige besturingssysteem
    os_type = platform.system()
    
    if os_type == "Windows":
        # Gebruik indices voor Windows
        for index in range(10):  # Check maximaal 10 indices
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:  # Zorg ervoor dat de camera frames levert
                    cameras.append(index)
                cap.release()
    elif os_type == "Linux":
        # Gebruik /dev/video* voor Linux
        for index in range(10):  # Controleer maximaal 10 apparaten
            path = f"/dev/video{index}"
            if os.path.exists(path):  # Controleer of het apparaatbestand bestaat
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:  # Controleer of de camera frames levert
                        cameras.append(index)
                    cap.release()

    root.config(cursor="")  # Reset cursor
    return cameras

# Function to save selected cameras to a JSON file
def save_selected_cameras():
    selected_cameras = []
    for var in camera_vars:
        if var[1].get():  # If the checkbox is selected
            selected_cameras.append({
                "index": var[0],  # Camera index
                "name": f"Camera {camera_vars.index(var) + 1}"  # Automatically assigned name
            })
    
    with open('selected_cameras.json', 'w') as file:
        json.dump(selected_cameras, file, indent=4)
    
    messagebox.showinfo("Info", "Selected cameras saved successfully")

# Function to show live feed from a camera
def show_camera_feed(port):
    root.config(cursor="watch")  # Show busy cursor
    root.update_idletasks()

    cap = cv2.VideoCapture(port)
    if not cap.isOpened():
        root.config(cursor="")  # Reset cursor
        messagebox.showerror("Error", f"Cannot open camera {port}")
        return

    root.config(cursor="")  # Reset cursor after opening the camera

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

# Function to center the window on the screen with adjusted dimensions
def center_window(root, width_percentage=0.25, height_percentage=0.4):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.attributes("-topmost", True)  # Keep on top initially
    root.after(100, lambda: root.attributes("-topmost", False))  # Allow other windows after focusing

# Initialize the main window
root = tk.Tk()
root.title("Find Connected Cameras")
center_window(root)

# Detect connected cameras
connected_cameras = detect_cameras()
camera_vars = []

# Create and grid the labels, checkboxes, and test buttons
for index, camera_index in enumerate(connected_cameras):
    camera_var = tk.BooleanVar()
    ttk.Label(root, text=f"Camera {index + 1} (Port {camera_index})").grid(row=index, column=0, padx=10, pady=5, sticky=tk.W)
    ttk.Checkbutton(root, variable=camera_var).grid(row=index, column=1, padx=10, pady=5, sticky=tk.W)
    test_button = ttk.Button(root, text="Test", command=lambda c=camera_index: show_camera_feed(c))
    test_button.grid(row=index, column=2, padx=10, pady=5, sticky=tk.W)
    camera_vars.append((camera_index, camera_var))

# Add Save button
save_button = ttk.Button(root, text="Save Selected Cameras", command=save_selected_cameras)
save_button.grid(row=len(connected_cameras), column=0, columnspan=3, padx=10, pady=10)

# Function to handle window close event
def on_closing():
    for window in open_camera_windows:
        try:
            if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow(window)
        except cv2.error as e:
            print(f"Error closing window {window}: {e}")
    open_camera_windows.clear()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
root.mainloop()
