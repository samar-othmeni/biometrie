
import cv2
import hashlib
import sqlite3
import os

def init_db():
    conn = sqlite3.connect("fingerprints.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    fingerprint_hash TEXT NOT NULL UNIQUE
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    fingerprint_hash TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

def load_image_and_hash(image_path):
    if not os.path.exists(image_path):
        print("Image introuvable.")
        return None
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Erreur lors du chargement de l'image.")
        return None
    img_resized = cv2.resize(img, (200, 200))
    hash_val = hashlib.sha256(img_resized).hexdigest()
    return hash_val

def register_fingerprint(image_path, name):
    hash_val = load_image_and_hash(image_path)
    if hash_val is None:
        return
    conn = sqlite3.connect("fingerprints.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, fingerprint_hash) VALUES (?, ?)", (name, hash_val))
        conn.commit()
        print("✅ Empreinte enregistrée avec succès.")
    except sqlite3.IntegrityError:
        print("❌ Cette empreinte est déjà enregistrée.")
    conn.close()

def verify_and_get_hash(image_path):
    hash_val = load_image_and_hash(image_path)
    if hash_val is None:
        return None
    conn = sqlite3.connect("fingerprints.db")
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE fingerprint_hash = ?", (hash_val,))
    result = c.fetchone()
    conn.close()
    if result:
        print(f">> Empreinte reconnue (utilisateur : {result[0]}).")
        return hash_val
    else:
        print("❌ Empreinte non reconnue.")
        print("[1] Enregistrer cette empreinte")
        print("[2] Annuler")
        choix = input("Choix : ")
        if choix == "1":
            name = input("Nom de l’utilisateur : ")
            register_fingerprint(image_path, name)
            return hash_val
        else:
            print("Opération annulée.")
            return None
