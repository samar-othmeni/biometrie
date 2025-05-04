# logger.py

import csv
from datetime import datetime

def log_event(empreinte: str, type_operation: str, resultat: str, type_acteur: str, fichier: str = ""):
    with open("logs.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            empreinte,
            type_operation,
            resultat,
            type_acteur,
            fichier,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
