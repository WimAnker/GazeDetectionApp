import os
import json
import cv2
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from ultralytics import YOLO

# Functie om de instellingen te laden vanuit een JSON-bestand
def load_settings():
    try:
        with open("SettingsAnnotateVideo.json", "r") as infile:
            settings = json.load(infile)
        return settings
    except FileNotFoundError:
        messagebox.showerror("Error", "Settings file not found. Please configure the settings first.")
        return None

# Functie om de video te annoteren en top 5 resultaten naar een CSV te schrijven
def annotate_video(settings):
    model_path = settings['model_path']
    video_path = settings['video_path']
    output_dir = settings['output_dir']
    output_filename = settings['output_filename']

    # Start annotatie
    print(f"Start annotatie voor {output_filename}")

    # Controleer of het modelbestand bestaat
    if not os.path.exists(model_path):
        messagebox.showerror("Error", f"Het modelbestand is niet gevonden op het pad: {model_path}")
        return

    # Laad het YOLOv8 model
    try:
        model = YOLO(model_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the model: {e}")
        return

    # Controleer of het videobestand bestaat
    if not os.path.exists(video_path):
        messagebox.showerror("Error", f"Het videobestand is niet gevonden op het pad: {video_path}")
        return

    # Open de video file
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        messagebox.showerror("Error", "Failed to open the video file.")
        return

    frame_number = 0
    annotations = []

    while True:
        ret, frame = video.read()
        if not ret:
            break  # Einde van de video

        # Voer de YOLO predictie uit op het frame
        results = model(frame)

        # Verwerk de probabiliteiten voor elk gedetecteerd object
        for result in results:
            if hasattr(result, 'probs') and result.probs is not None:
                probs = result.probs

                # Voeg de top-5 klassen en hun confidentie toe
                top5_class_indices = probs.top5  # Indexen van de top 5 klassen
                top5_confidences = probs.top5conf  # Confidentie van de top 5 klassen

                # Verwerk elke top 5 klasse en confidentie
                frame_data = [frame_number]
                for idx, conf in zip(top5_class_indices, top5_confidences):
                    label = model.names[idx]  # Haal het corresponderende label op
                    confidence = float(conf) * 100  # Convert naar percentage
                    frame_data.append(f"{label},{confidence:.2f}")
                
                annotations.append(frame_data)

        frame_number += 1

    video.release()

    # Schrijf de annotaties naar een CSV-bestand
    output_csv_path = os.path.join(output_dir, f"{output_filename}.csv")
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Top1 (Label, Confidence)", "Top2 (Label, Confidence)", "Top3 (Label, Confidence)", "Top4 (Label, Confidence)", "Top5 (Label, Confidence)"])
        writer.writerows(annotations)

    print(f"Eind annotatie. Output opgeslagen in: {output_csv_path}")
    messagebox.showinfo("Success", f"Video annotatie voltooid. CSV output opgeslagen in: {output_csv_path}")

# Functie om het venster te centreren op het scherm
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Annotatie venster openen direct bij opstarten
def open_annotate_video_window():
    settings = load_settings()
    if settings is None:
        return  # Instellingen niet gevonden, functie afsluiten

    root = tk.Tk()
    root.title("Annotate Video (Model Based)")

    # Toon de paden vanuit de instellingen
    ttk.Label(root, text="Model Path:").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['model_path']).grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(root, text="Video Path:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['video_path']).grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['output_dir']).grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(root, text="Output Filename:").grid(row=3, column=0, padx=10, pady=10)
    ttk.Label(root, text=settings['output_filename']).grid(row=3, column=1, padx=10, pady=10)

    # Knop om de annotatie te starten
    annotate_button = ttk.Button(root, text="Annotate", command=lambda: annotate_video(settings))
    annotate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

    # Venster centreren
    center_window(root)

    root.mainloop()

# Start de annotatie window direct
open_annotate_video_window()
