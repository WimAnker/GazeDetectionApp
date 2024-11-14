import tkinter as tk
from tkinter import messagebox
import sys

# Initialiseer de Tkinter root
root = tk.Tk()
root.withdraw()  # Verberg het hoofdvenster

# Centreer de messagebox op basis van de opgegeven parameters
if len(sys.argv) == 5:
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])

    # Bereken de positie voor het centreren van de messagebox
    root.geometry(f"+{x + width // 2}+{y + height // 2}")

# Toon de messagebox met de gewenste boodschap
messagebox.showinfo(
    "Comparison Not Available",
    "The automatic comparison between audio and model annotation is (yet) not developed. The comparison between the two outputs has been performed manually in Excel."
)

# Sluit het venster
root.quit()
