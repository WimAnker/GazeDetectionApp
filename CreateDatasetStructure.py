import os
import json

# Function to load settings from a JSON file
def load_settings():
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        print("No saved settings found")
        return None

# Function to load labels from a JSON file
def load_labels():
    try:
        with open('label_data.json', 'r') as file:
            labels = json.load(file)
        return labels
    except FileNotFoundError:
        print("No saved labels found")
        return None

# Function to create the directory structure for the dataset
def create_dataset_structure(base_path, labels):
    training_data_path = os.path.join(base_path, "trainingsdata")
    dataset_path = os.path.join(training_data_path, "dataset")

    # Create root directories
    os.makedirs(training_data_path, exist_ok=True)
    os.makedirs(dataset_path, exist_ok=True)

    # Create subdirectories for train, test, and val
    for subset in ["train", "test", "val"]:
        subset_path = os.path.join(dataset_path, subset)
        os.makedirs(subset_path, exist_ok=True)

        # Create label subdirectories within each subset
        for label in labels:
            if label[-1]:  # Only create directories for labels that are marked for use
                label_name = label[0]
                label_path = os.path.join(subset_path, label_name)
                os.makedirs(label_path, exist_ok=True)

    print(f"Dataset directory structure created at {dataset_path}")

# Load settings and labels
settings = load_settings()
labels = load_labels()

if not settings or not labels:
    print("Settings or labels could not be loaded. Exiting...")
    exit(1)

# Ensure all required settings are present
required_settings = ["base_path"]
for setting in required_settings:
    if setting not in settings:
        print(f"Missing setting: {setting}")
        exit(1)

base_path = settings["base_path"]

# Create the dataset directory structure
create_dataset_structure(base_path, labels)
