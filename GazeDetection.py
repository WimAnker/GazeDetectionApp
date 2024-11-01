import os
import json
import tkinter as tk
from tkinter import Menu, messagebox
import subprocess
import platform

# Bepaal de juiste Python-opdracht op basis van het besturingssysteem
python_command = "python" if platform.system() == "Windows" else "python3"

# Functie om externe scripts uit te voeren met de positie van het hoofdvenster
def run_script(script_name, root):
    try:
        print(f"Attempting to run: {script_name}")  # Debug statement
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()
        p = subprocess.Popen([python_command, script_name, str(x), str(y), str(width), str(height)])
        subprocesses.append(p)
        p.wait()  # Wacht tot het script klaar is
    except Exception as e:
        print(f"Failed to run {script_name}: {e}")

# Functies om externe scripts aan te roepen:
def collect_data_settings():
    run_script('RecordingSettings.py', root)

def setup_labels():
    run_script('SetupLabels.py', root)

def collect_data_cameras_positioning():
    run_script('FindCameras.py', root)

def collect_data_start_recording_script():
    run_script('StartRecording.py', root)

# Prepare Data
def prepare_settings():
    run_script('PrepareSettings.py', root)

def prepare_data_for_training():
    run_script('PrepareDataset.py', root)

# Create Video
def start_recording_testvideo():
    run_script('StartRecordingTestvideo.py', root)

def settings_testvideo():
    run_script('SettingsTestvideo.py', root)

# Annotate Video (model based)
def settings_annotate_video():
    run_script('SettingsAnnotateVideo.py', root)

def annotate_video():
    run_script('AnnotateVideo.py', root)

# Annotate Video (audio based)
def annotate_video_audio():
    run_script('AnnotateVideoAudio.py', root)

def compare_test_and_model_annotation():
    run_script('CompareTestAndModelAnnotation.py', root)

# Functie om het hoofdvenster te centreren
def center_window(root, width_percentage=0.5, height_percentage=0.5):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * width_percentage)
    height = int(screen_height * height_percentage)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

# Functie om venster sluiting af te handelen
def on_closing():
    for p in subprocesses:
        p.terminate()
    root.destroy()

# Initialiseer het hoofdvenster
root = tk.Tk()
root.title("Application")

# Centreer en pas venstergrootte aan
center_window(root)

# Lijst om subprocessen bij te houden
subprocesses = []

# Menu bar maken
menu_bar = Menu(root)

# Voeg de submenu's toe zoals eerder
create_data_menu = Menu(menu_bar, tearoff=0)
create_data_menu.add_command(label="Settings Recording", command=collect_data_settings)
create_data_menu.add_command(label="Setup Labels", command=setup_labels)
create_data_menu.add_command(label="Cameras and Positioning", command=collect_data_cameras_positioning)
create_data_menu.add_command(label="Start Recording Script", command=collect_data_start_recording_script)
menu_bar.add_cascade(label="Create Data", menu=create_data_menu)

prepare_data_menu = Menu(menu_bar, tearoff=0)
prepare_data_menu.add_command(label="Settings for Prepare Data", command=prepare_settings)
prepare_data_menu.add_command(label="Prepare Data for Training", command=prepare_data_for_training)
menu_bar.add_cascade(label="Prepare Data", menu=prepare_data_menu)

create_video_menu = Menu(menu_bar, tearoff=0)
create_video_menu.add_command(label="Settings Video", command=settings_testvideo)
create_video_menu.add_command(label="Recording Video", command=start_recording_testvideo)
menu_bar.add_cascade(label="Create Video", menu=create_video_menu)

# "Annotate Video" submenu
annotate_video_menu = Menu(menu_bar, tearoff=0)
annotate_video_menu.add_command(label="Settings Annotate Video", command=settings_annotate_video)
annotate_video_menu.add_command(label="Annotate Video (model based)", command=annotate_video)
annotate_video_menu.add_command(label="Annotate Video (audio based)", command=annotate_video_audio)
menu_bar.add_cascade(label="Annotate Video", menu=annotate_video_menu)

menu_bar.add_command(label="Compare Video- and Model Annotation", command=compare_test_and_model_annotation)

root.config(menu=menu_bar)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start de hoofdlus
root.mainloop()
