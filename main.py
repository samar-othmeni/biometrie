from biometric_module import init_db, register_fingerprint, verify_and_get_hash
from encryption_module import encrypt_file, decrypt_file
from logger import log_event

def main():
    init_db()
    while True:
        print("\n--- MENU ---")
        print("1. Enregistrer une empreinte")
        print("2. Chiffrer un fichier")
        print("3. Déchiffrer un fichier")
        print("4. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            image = input("Chemin de l'image d'empreinte : ")
            name = input("Nom : ")
            register_fingerprint(image, name)
            # Optionnel : tu peux aussi logguer l'enregistrement
            log_event(name, "enregistrement", "réussi", "autorisé")

        elif choix == "2":
            image = input("Chemin de l'image d'empreinte : ")
            hash_val = verify_and_get_hash(image)
            if hash_val:
                fichier = input("Chemin du fichier à chiffrer : ")
                encrypt_file(fichier, hash_val)
                log_event(image, "chiffrement", "réussi", "autorisé", fichier)
            else:
                log_event(image, "chiffrement", "échoué", "non autorisé")
        
        elif choix == "3":
            image = input("Chemin de l'image d'empreinte : ")
            hash_val = verify_and_get_hash(image)
            if hash_val:
                fichier = input("Chemin du fichier chiffré (.enc) : ")
                try:
                    decrypt_file(fichier, hash_val)
                    log_event(image, "déchiffrement", "réussi", "autorisé", fichier)
                except ValueError as e:
                    print(f" {e}")
                    log_event(image, "déchiffrement", "échoué", "non autorisé", fichier)
            else:
                print("❌ Empreinte inconnue.")
                log_event(image, "déchiffrement", "échoué", "intrus")
                
        elif choix == "4":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()










# from biometric_module import init_db, register_fingerprint, verify_and_get_hash
# from encryption_module import encrypt_file, decrypt_file

# def main():
#     init_db()
#     while True:
#         print("\n--- MENU ---")
#         print("1. Enregistrer une empreinte")
#         print("2. Chiffrer un fichier")
#         print("3. Déchiffrer un fichier")
#         print("4. Quitter")
#         choix = input("Choix : ")

#         if choix == "1":
#             image = input("Chemin de l'image d'empreinte : ")
#             name = input("Nom : ")
#             register_fingerprint(image, name)
#         elif choix == "2":
#             image = input("Chemin de l'image d'empreinte : ")
#             hash_val = verify_and_get_hash(image)
#             if hash_val:
#                 fichier = input("Chemin du fichier à chiffrer : ")
#                 encrypt_file(fichier, hash_val)
#         elif choix == "3":
#             image = input("Chemin de l'image d'empreinte : ")
#             hash_val = verify_and_get_hash(image)
#             if hash_val:
#                 fichier = input("Chemin du fichier chiffré (.enc) : ")
#                 decrypt_file(fichier, hash_val)
#         elif choix == "4":
#             print("Au revoir.")
#             break
#         else:
#             print("Choix invalide.")

# if __name__ == "__main__":
#     main()
