import os
import csv
import subprocess
import whisper
import json
import tkinter as tk
from tkinter import ttk, messagebox

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

# Functie om de video te annoteren op basis van audio en resultaten naar een CSV-bestand te schrijven
def annotate_video_audio(settings, labels):
    video_path = settings["video_path"]
    output_dir = settings["output_dir"]
    output_filename = settings["output_filename"]
    audio_path = os.path.join(output_dir, "extracted_audio.wav")
    output_csv = os.path.join(output_dir, f"{output_filename}.csv")

    # Extract audio from video
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"], check=True)

    # Laad het Whisper-model
    model = whisper.load_model("medium")

    # Transcribeer de audio
    result = model.transcribe(audio_path)

    # Verwijder het audiobestand na de transcriptie
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Definieer de nummers om naar te zoeken
    nummers_zoeken = {
        "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", 
        "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten", 
        "11": "eleven", "12": "twelve"
    }

    # Zoek naar de nummers en sla ze op in timestamps
    timestamps = []
    frames_per_second = 30  # Stel de framerate van de video in
    frame_counter = 0

    for segment in result["segments"]:
        text = segment["text"].lower()
        start_time = segment["start"]
        end_time = segment["end"]
        start_frame = frame_counter
        end_frame = start_frame + int((end_time - start_time) * frames_per_second)
        frame_counter = end_frame

        for num, word in nummers_zoeken.items():
            if num in text or word in text:
                label = labels.get(num, "Unknown")  # Gebruik het label in plaats van de zin
                timestamps.append((start_time, num, label, start_frame, end_frame))

    # Schrijf resultaten naar CSV
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
