import os
import json
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import random
import shutil
import threading
import sys

# Function to load settings from a JSON file
def load_settings():
    try:
        with open('prepare_settings.json', 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        print("No saved settings found")
        return None

# Function to create necessary directories
def create_directories(base_path, prepare_name, labels):
    dataset_path = os.path.join(base_path, prepare_name, "dataset")
    train_path = os.path.join(dataset_path, "train")
    test_path = os.path.join(dataset_path, "test")
    val_path = os.path.join(dataset_path, "val")
    
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)

    for label in labels:
        os.makedirs(os.path.join(train_path, label), exist_ok=True)
        os.makedirs(os.path.join(test_path, label), exist_ok=True)
        os.makedirs(os.path.join(val_path, label), exist_ok=True)

    return train_path, test_path, val_path, dataset_path

# Function to extract frames from videos
def extract_frames(video_path, output_path, label, cycle, extraction_frequency, metadata_list, frame_counts):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_count = 0
    video_name = os.path.basename(video_path).split('.')[0]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % extraction_frequency == 0:
            frame_filename = f"{label}_cycle_{cycle}_{video_name}_frame{frame_count}.jpg"
            frame_path = os.path.join(output_path, frame_filename)
            cv2.imwrite(frame_path, frame)
            extracted_count += 1

            # Add metadata entry
            metadata = {
                "label": label,
                "cycle": cycle,
                "filename": frame_filename,
                "frame_number": frame_count,
                "video_path": video_path
            }
            metadata_list.append(metadata)

        frame_count += 1

    # Update frame counts
    if label not in frame_counts:
        frame_counts[label] = {"train": 0, "test": 0, "val": 0}
    frame_counts[label]["train"] += extracted_count

    cap.release()
    return extracted_count

# Function to distribute frames using stratified sampling
def distribute_frames(train_path, test_path, val_path, labels, test_percentage, val_percentage, frame_counts):
    for label in labels:
        label_train_path = os.path.join(train_path, label)
        label_test_path = os.path.join(test_path, label)
        label_val_path = os.path.join(val_path, label)

        all_frames = os.listdir(label_train_path)
        total_frames = len(all_frames)
        num_test = int(total_frames * test_percentage / 100)
        num_val = int(total_frames * val_percentage / 100)

        test_frames = random.sample(all_frames, num_test)
        val_frames = random.sample([frame for frame in all_frames if frame not in test_frames], num_val)

        for frame in test_frames:
            shutil.move(os.path.join(label_train_path, frame), os.path.join(label_test_path, frame))
            frame_counts[label]["train"] -= 1
            frame_counts[label]["test"] += 1

        for frame in val_frames:
            shutil.move(os.path.join(label_train_path, frame), os.path.join(label_val_path, frame))
            frame_counts[label]["train"] -= 1
            frame_counts[label]["val"] += 1

def process_dataset():
    root.config(cursor="wait")

    # Load settings
    prepare_settings = load_settings()
    if not prepare_settings:
        print("Settings could not be loaded. Exiting...")
        root.config(cursor="")
        return

    # Ensure all required settings are present
    required_settings = ["extraction_frequency", "base_path", "prepare_name", "test_percentage", "val_percentage"]
    for setting in required_settings:
        if setting not in prepare_settings:
            print(f"Missing setting: {setting}")
            root.config(cursor="")
            return

    extraction_frequency = int(prepare_settings["extraction_frequency"])
    base_path = prepare_settings["base_path"]
    prepare_name = prepare_settings["prepare_name"]
    test_percentage = int(prepare_settings["test_percentage"])
    val_percentage = int(prepare_settings["val_percentage"])

    # Determine the paths
    recording_base_path = os.path.join(base_path, prepare_name, "Recording")
    if not os.path.exists(recording_base_path):
        print(f"The path {recording_base_path} does not exist.")
        root.config(cursor="")
        return

    labels = [d for d in os.listdir(recording_base_path) if os.path.isdir(os.path.join(recording_base_path, d))]
    train_path, test_path, val_path, dataset_path = create_directories(base_path, prepare_name, labels)

    metadata_list = []
    frame_counts = {}

    # Iterate over all labels and subdirectories
    for label in labels:
        label_path = os.path.join(recording_base_path, label)
        if os.path.isdir(label_path):
            for cycle in os.listdir(label_path):
                cycle_path = os.path.join(label_path, cycle)
                if os.path.isdir(cycle_path):
                    for video_file in os.listdir(cycle_path):
                        if video_file.endswith(('.mp4', '.avi')):
                            video_path = os.path.join(cycle_path, video_file)
                            output_path = os.path.join(train_path, label)
                            extracted_count = extract_frames(video_path, output_path, label, cycle, extraction_frequency, metadata_list, frame_counts)
                            print(f"Extracted {extracted_count} frames from {video_file} in {label}/cycle_{cycle}")

    # Distribute frames to test and val directories
    distribute_frames(train_path, test_path, val_path, labels, test_percentage, val_percentage, frame_counts)

    # Write metadata and frame counts to the readme.txt file
    readme_path = os.path.join(dataset_path, "readme.txt")
    with open(readme_path, 'w') as f:
        for meta in metadata_list:
            f.write(json.dumps(meta, indent=4) + '\n')
        f.write("\nFrame Counts by Label:\n")
        for label, counts in frame_counts.items():
            f.write(f"Label: {label}, Train: {counts['train']}, Test: {counts['test']}, Val: {counts['val']}\n")

    print("Frame extraction and distribution completed.")
    root.config(cursor="")
    messagebox.showinfo("Info", "Dataset processing completed successfully")

# Function to center the window relative to the main window
def center_window(root, main_x, main_y, main_width, main_height, width_percentage=0.4, height_percentage=0.5):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = main_x + (main_width // 2) - (width // 2)
    y = main_y + (main_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Main application window
root = tk.Tk()
root.title("Prepare Dataset")

# Get the main window's position and size from the command line arguments
main_x = int(sys.argv[1])
main_y = int(sys.argv[2])
main_width = int(sys.argv[3])
main_height = int(sys.argv[4])

# Center and resize the window relative to the main window
center_window(root, main_x, main_y, main_width, main_height)

# Add Process Dataset button
process_button = ttk.Button(root, text="Process Dataset", command=lambda: threading.Thread(target=process_dataset).start())
process_button.pack(padx=20, pady=20)

# Run the main event loop
root.mainloop()
