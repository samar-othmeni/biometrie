
# import base64
# import hashlib
# from cryptography.fernet import Fernet
# import sqlite3

# def encrypt_file(file_path, hash_val):
#     with open(file_path, "rb") as f:
#         data = f.read()
#     key = hashlib.sha256(hash_val.encode()).digest()
#     fernet = Fernet(base64.urlsafe_b64encode(key[:32]))
#     encrypted = fernet.encrypt(data)
#     with open(file_path + ".enc", "wb") as f:
#         f.write(encrypted)
#     print(f"✅ Fichier chiffré et sauvegardé sous : {file_path}.enc")

#     conn = sqlite3.connect("fingerprints.db")
#     c = conn.cursor()
#     c.execute("INSERT INTO files (file_path, fingerprint_hash) VALUES (?, ?)", (file_path + ".enc", hash_val))
#     conn.commit()
#     conn.close()

# def decrypt_file(file_path, hash_val):
#     conn = sqlite3.connect("fingerprints.db")
#     c = conn.cursor()
#     c.execute("SELECT fingerprint_hash FROM files WHERE file_path = ?", (file_path,))
#     result = c.fetchone()
#     conn.close()

#     # if not result:
#     #     print("❌ Fichier non reconnu ou pas enregistré.")
#     #     return

#     if not result:
#         raise ValueError("Fichier non reconnu ou pas enregistré.")


#     original_hash = result[0]
#     # if original_hash != hash_val:
#     #     print("❌ Cette empreinte n’a pas chiffré ce fichier. Accès refusé.")
#     #     return
#     if original_hash != hash_val:
#         raise ValueError("Cette empreinte n’a pas chiffré ce fichier. Accès refusé.")


#     with open(file_path, "rb") as f:
#         encrypted_data = f.read()
#     key = hashlib.sha256(hash_val.encode()).digest()
#     fernet = Fernet(base64.urlsafe_b64encode(key[:32]))
#     try:
#         decrypted_data = fernet.decrypt(encrypted_data)
#         original_file = file_path.replace(".enc", ".dec")
#         with open(original_file, "wb") as f:
#             f.write(decrypted_data)
#         print(f"✅ Fichier déchiffré et sauvegardé sous : {original_file}")
#     except Exception as e:
#         print(f"Erreur de déchiffrement : {e}")




import base64
import hashlib
from cryptography.fernet import Fernet
import sqlite3

def encrypt_file(file_path, hash_val):
    with open(file_path, "rb") as f:
        data = f.read()
    key = hashlib.sha256(hash_val.encode()).digest()
    fernet = Fernet(base64.urlsafe_b64encode(key[:32]))
    encrypted = fernet.encrypt(data)
    with open(file_path + ".enc", "wb") as f:
        f.write(encrypted)
    print(f"✅ Fichier chiffré et sauvegardé sous : {file_path}.enc")

    conn = sqlite3.connect("fingerprints.db")
    c = conn.cursor()
    c.execute("INSERT INTO files (file_path, fingerprint_hash) VALUES (?, ?)", (file_path + ".enc", hash_val))
    conn.commit()
    conn.close()

def decrypt_file(file_path, hash_val):
    conn = sqlite3.connect("fingerprints.db")
    c = conn.cursor()
    c.execute("SELECT fingerprint_hash FROM files WHERE file_path = ?", (file_path,))
    result = c.fetchone()
    conn.close()

    if not result:
        raise ValueError("❌ Fichier non reconnu ou pas enregistré.")

    original_hash = result[0]
    if original_hash != hash_val:
        raise ValueError("❌ Cette empreinte n’a pas chiffré ce fichier. Accès refusé.")

    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    key = hashlib.sha256(hash_val.encode()).digest()
    fernet = Fernet(base64.urlsafe_b64encode(key[:32]))
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        original_file = file_path.replace(".enc", ".dec")
        with open(original_file, "wb") as f:
            f.write(decrypted_data)
        print(f"✅ Fichier déchiffré et sauvegardé sous : {original_file}")
    except Exception as e:
        raise ValueError(f"Erreur de déchiffrement : {e}")

