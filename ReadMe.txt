# Gaze Detection Application

Dit project bevat een desktop applicatie geschreven in Python, gebruikmakend van Tkinter. Volg de onderstaande stappen om de applicatie op je eigen computer te installeren en uit te voeren.

## Vereisten

- Python 3.x
- Tkinter (meestal standaard inbegrepen bij Python)
- Vereiste Python-pakketten (zie `requirements_linux.txt` of `requirements_windows.txt`, afhankelijk van je besturingssysteem)

## Installatie en Uitvoering

### Windows

1. **Download en installeer Python**:
   - Ga naar [python.org](https://www.python.org/) en download de nieuwste versie van Python voor Windows.
   - Zorg ervoor dat je de optie selecteert om Python toe te voegen aan het pad tijdens de installatie.

2. **Download de projectbestanden**:
   - Download de projectmap van OSF en pak de bestanden uit naar een gewenste locatie op je computer.
   
    OF

   - Ga naar de GazeDetectionApp GitHub repository: https://github.com/WimAnker/GazeDetectionApp en download de bestanden door te klikken op de groene knop **Code** en te kiezen voor **Download ZIP**. (Zorg ervoor dat je de `master` branch geselecteerd hebt als dat nodig is).
   - Pak de gedownloade ZIP-bestanden uit naar een gewenste locatie op je computer.

3. **Installeer vereiste pakketten**:
   - Open een command prompt (cmd) en navigeer naar de map waar je de projectbestanden hebt uitgepakt.
   - Voer het volgende commando uit om de benodigde pakketten te installeren:
     ```sh
     pip install -r requirements_windows.txt
     ```

4. **Voer de applicatie uit**:
   - Run het hoofd Python-bestand:
     ```sh
     python GazeDetection.py
     ```

### Linux

1. **Zorg ervoor dat Python is geïnstalleerd**:
   - Controleer of Python is geïnstalleerd door het volgende commando in de terminal uit te voeren:
     ```sh
     python3 --version
     ```
   - Als Python niet is geïnstalleerd, kun je het installeren met:
     ```sh
     sudo apt update
     sudo apt install python3
     ```

2. **Installeer Tkinter**:
   - Installeer Tkinter als het nog niet is geïnstalleerd:
     ```sh
     sudo apt install python3-tk
     ```

3. **Installeer de vereisten voor PyAudio**:
   - Voordat je `PyAudio` installeert, moet je eerst `portaudio19-dev` installeren:
     ```sh
     sudo apt-get install portaudio19-dev
     ```

4. **Download de projectbestanden**:
   - Ga naar de GazeDetectionApp GitHub repository: https://github.com/WimAnker/GazeDetectionApp en download de bestanden door te klikken op de groene knop **Code** en te kiezen voor **Download ZIP**. (Zorg ervoor dat je de `master` branch geselecteerd hebt als dat nodig is).
   - Pak de gedownloade ZIP-bestanden uit naar een gewenste locatie op je computer.

5. **Installeer vereiste pakketten**:
   - Navigeer naar de map waar je de projectbestanden hebt uitgepakt.
   - Voer het volgende commando uit om de benodigde pakketten te installeren:
     ```sh
     pip3 install -r requirements_linux.txt
     ```

6. **Voer de applicatie uit**:
   - Run het hoofd Python-bestand:
     ```sh
     python3 GazeDetection.py
     ```

## Contact

Voor vragen of problemen, neem contact op met de projectbeheerder via GitHub.
