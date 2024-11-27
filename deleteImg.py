import os

input_folder = "_photos/photos/min"

for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Vérifie que le fichier est une image
        if os.path.isfile(input_path) and filename.lower().endswith(('.jpg')):
            os.remove(os.path.join(input_folder, filename))