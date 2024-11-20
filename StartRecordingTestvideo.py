import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pyttsx3
import json

# Functie om camera-apparaatnamen te laden uit JSON
def load_camera_names():
    if os.path.exists("camera_names.json"):
        with open("camera_names.json", "r") as json_file:
            return json.load(json_file)
    else:
        messagebox.showerror("Error", "camera_names.json not found.")
        return {"video_device": "", "audio_device": ""}

# Functie om de instellingen uit de JSON-file te laden
def load_settings():
    if os.path.exists("compare_settings.json"):
        with open("compare_settings.json", "r") as json_file:
            return json.load(json_file)
    else:
        messagebox.showerror("Error", "Settings file not found.")
        return {}

# Functie om labels te laden uit de JSON-file
def load_labels():
    if os.path.exists("label_data.json"):
        with open("label_data.json", "r") as json_file:
            labels_data = json.load(json_file)
            selected_labels = [(label[2], label[4]) for label in labels_data if label[-1]]
            return selected_labels
    else:
        messagebox.showerror("Error", "Labels file not found.")
        return []

# Functie om het venster te centreren op het scherm
def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Functie om opname met zinnen te starten
def start_recording_with_sentences():
    start_button_sentences.config(state=tk.DISABLED)

    settings = load_settings()
    camera_names = load_camera_names()
    selected_labels = load_labels()
    
    if not settings or not selected_labels or not camera_names.get("video_device") or not camera_names.get("audio_device"):
        return

    video_device = camera_names["video_device"]
    audio_device = camera_names["audio_device"]

    num_sentences = int(settings.get("num_sentences", len(selected_labels)))
    interval_seconds = int(settings.get("interval_seconds", 5))
    extra_time_seconds = 5

    output_path = settings.get("path", "")
    base_name = settings.get("name", "output_sentences")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    duration = num_sentences * interval_seconds + extra_time_seconds

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 80)
    
    output_file = os.path.join(output_path, f"{base_name}_usb_camera.mp4")

    # FFmpeg-opdracht met apparaten uit JSON
    ffmpeg_command = (
        f'ffmpeg -y -f dshow -audio_buffer_size 50 -rtbufsize 512M '
        f'-i video="{video_device}":audio="{audio_device}" '
        f'-t {duration} -c:v libx264 -c:a aac -ar 44100 -async 1 "{output_file}"'
    )

    print(f"Running FFmpeg command: {ffmpeg_command}")

    process = subprocess.Popen(ffmpeg_command, shell=True)

    for i, (_, sentence) in enumerate(selected_labels[:num_sentences]):
        engine.say(sentence)
        engine.runAndWait()
        progress_label.config(text=f"Sentences: {i+1}/{num_sentences}")
        root.update_idletasks()
        time.sleep(interval_seconds)
    
    time.sleep(extra_time_seconds)

    process.wait()

    messagebox.showinfo("Info", f"Opname voltooid! Video opgeslagen in: {output_file}")
    start_button_sentences.config(state=tk.NORMAL)

# Functie om een opname zonder zinnen te starten en handmatig te stoppen
def start_recording_no_sentences():
    start_button_live.config(state=tk.DISABLED)
    stop_button_live.config(state=tk.NORMAL)

    settings = load_settings()
    camera_names = load_camera_names()

    if not settings or not camera_names.get("video_device") or not camera_names.get("audio_device"):
        return

    video_device = camera_names["video_device"]
    audio_device = camera_names["audio_device"]

    output_path = settings.get("path", "")
    base_name = settings.get("name", "output_no_sentences")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    global output_file
    output_file = os.path.join(output_path, f"{base_name}_usb_camera.mp4")

    # FFmpeg-opdracht met apparaten uit JSON
    ffmpeg_command = (
        f'ffmpeg -y -f dshow -audio_buffer_size 50 -rtbufsize 512M '
        f'-i video="{video_device}":audio="{audio_device}" '
        f'-t 3600 -c:v libx264 -c:a aac -ar 44100 -async 1 "{output_file}"'
    )

    print(f"Running FFmpeg command: {ffmpeg_command}")

    global process
    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, shell=True)
    global start_time
    start_time = time.time()

# Functie om de opname zonder zinnen te stoppen
def stop_recording_no_sentences():
    global process, output_file
    if process:
        # Schrijf 'q' naar het proces om het netjes af te sluiten
        process.stdin.write(b'q')
        process.stdin.flush()
        process.wait()  # Wacht tot het proces is beëindigd

        process = None
        messagebox.showinfo("Info", f"Opname zonder zinnen gestopt en opgeslagen in: {output_file}")
        stop_button_live.config(state=tk.DISABLED)
        start_button_live.config(state=tk.NORMAL)

# Initialiseer het hoofdvenster
root = tk.Tk()
root.title("Start Recording Video")

instruction_label = ttk.Label(root, text="Sluit de camera aan op de linker USB-poort! \n"
                                         "(Check eventueel via de applicatie Logitech App of de camera wordt herkend en correct is gepositioneerd).")
instruction_label.pack(pady=10)

progress_label = ttk.Label(root, text="Sentences: 0/0")
progress_label.pack(pady=10)

start_button_sentences = ttk.Button(root, text="Start Recording With Sentences", command=start_recording_with_sentences)
start_button_sentences.pack(expand=True, padx=20, pady=5)

start_button_live = ttk.Button(root, text="Start Recording No Sentences", command=start_recording_no_sentences)
start_button_live.pack(expand=True, padx=20, pady=5)

stop_button_live = ttk.Button(root, text="Stop Recording", command=stop_recording_no_sentences, state=tk.DISABLED)
stop_button_live.pack(expand=True, padx=20, pady=5)

center_window(root)

root.mainloop()
