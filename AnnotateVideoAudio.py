import os
import csv
import subprocess
import whisper
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pydub import AudioSegment
import numpy as np
import re

# Functie om de instellingen te laden vanuit een JSON-bestand
def load_settings():
    try:
        with open("SettingsAnnotateVideo.json", "r") as infile:
            settings = json.load(infile)
        return settings
    except FileNotFoundError:
        messagebox.showerror("Error", "Settings file not found. Please configure the settings first.")
        return None

# Functie om de labels te laden uit een JSON-bestand
def load_labels():
    label_data_path = r"C:\Users\Gebruiker\GazeDetectionApp\label_data.json"
    with open(label_data_path, 'r') as f:
        label_data = json.load(f)
    return {str(i + 1): item[0] for i, item in enumerate(label_data)}  # Kolom 1 bevat het label

# Functie om de video-informatie op te halen
def get_video_info(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", 
             "stream=duration,nb_frames", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output = result.stdout.decode().splitlines()
        duration = float(output[0])  # Duur in seconden
        total_frames = int(output[1]) if len(output) > 1 and output[1].isdigit() else "unknown"
        print(f"Video duration: {duration} seconds", flush=True)
        print(f"Total frames: {total_frames}", flush=True)
        return duration, total_frames
    except Exception as e:
        print(f"Error retrieving video info: {e}", flush=True)
        return None, None

# Functie om audio om te zetten naar een NumPy array
def audiosegment_to_numpy(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    return samples.astype(np.float32) / np.iinfo(audio_segment.array_type).max

# Functie om te controleren of een audiogedeelte luid genoeg is
def is_segment_loud_enough(audio_segment, volume_threshold):
    return audio_segment.dBFS > volume_threshold

# Functie om de video te annoteren op basis van audio en resultaten naar een CSV-bestand te schrijven
def annotate_video_audio(settings, labels):
    print("Starting annotation process...", flush=True)
    video_path = settings["video_path"]
    output_dir = settings["output_dir"]
    output_filename = settings["output_filename"]
    audio_path = os.path.join(output_dir, "extracted_audio.wav")
    output_csv = os.path.join(output_dir, f"{output_filename}.csv")

    # Print de video-informatie
    duration, total_frames = get_video_info(video_path)
    frames_per_second = 30  # Stel de framerate van de video in

    # Extract de volledige audio van de video
    print("Extracting audio from video using ffmpeg...", flush=True)
    subprocess.run(["ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-y", audio_path], check=True)

    # Laad de volledige audio met pydub
    audio = AudioSegment.from_file(audio_path)

    # Filter audio op volume
    volume_threshold = -40  # Drempelwaarde in dBFS (kan worden aangepast)
    if not is_segment_loud_enough(audio, volume_threshold):
        print("Audio segment is too quiet and will be skipped.", flush=True)
        messagebox.showwarning("Warning", "The audio is too quiet to process.")
        return

    # Converteer de volledige audio naar een NumPy array
    audio_data = audiosegment_to_numpy(audio)

    # Laad het Whisper-model
    model = whisper.load_model("small")

    # Transcribeer de volledige audio
    print("Transcribing full audio...", flush=True)
    result = model.transcribe(audio_data, language="en")

    # Definieer de nummers om naar te zoeken
    nummers_zoeken = {
        "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", 
        "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten", 
        "11": "eleven", "12": "twelve"
    }

    timestamps = []

    # Verwerk de transcriptieresultaten
    for segment in result["segments"]:
        text = segment["text"].lower()
        start_time = segment["start"]
        end_time = segment["end"]

        start_frame = int(start_time * frames_per_second)
        end_frame = int(end_time * frames_per_second)

        for num, word in nummers_zoeken.items():
            if re.search(r'\b' + re.escape(num) + r'\b', text) or re.search(r'\b' + re.escape(word) + r'\b', text):
                label = labels.get(num, "Unknown")
                timestamps.append((start_time, num, label, start_frame, end_frame))

    print("Writing results to CSV...", flush=True)
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp (s)", "Nummer", "Label", "Start Frame", "End Frame"])
        for timestamp, nummer, label, start_frame, end_frame in timestamps:
            writer.writerow([timestamp, nummer, label, start_frame, end_frame])

    messagebox.showinfo("Success", f"Video annotatie voltooid. CSV output opgeslagen in: {output_csv}")

# Functie om het venster te centreren op het scherm
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Annotatie venster openen direct bij opstarten
def open_annotate_video_audio_window():
    settings = load_settings()
    if settings is None:
        return  # Instellingen niet gevonden, functie afsluiten

    labels = load_labels()

    root = tk.Tk()
    root.title("Annotate Video (Audio Based)")

    # Toon de paden vanuit de instellingen
    ttk.Label(root, text="Video Path:").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['video_path']).grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['output_dir']).grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(root, text="Output Filename:").grid(row=2, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['output_filename']).grid(row=2, column=1, padx=10, pady=10)

    # Knop om de annotatie te starten
    annotate_button = ttk.Button(root, text="Annotate", command=lambda: annotate_video_audio(settings, labels))
    annotate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    # Venster centreren
    center_window(root)

    root.mainloop()

# Start de annotatie window direct
open_annotate_video_audio_window()
