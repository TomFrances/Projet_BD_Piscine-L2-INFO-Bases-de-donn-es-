#!/usr/bin/python3

import os
from utils import db, m1, m2, m3, m4, m5, m6

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    # Nom de la BD à créer
    db_file = "data/piscine.db"

    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)

    # Remplir la BD
    print("Bienvenue dans l'application de gestion de notre base de données")
    create=input("Souhaitez-vous recréer la base de données (perte des modifications précédentes) (o/n) ? ")
    while create != 'o' and create != 'n':
        create = input("Souhaitez-vous recréer la base de données (perte des modifications précédentes) (o/n) ? ")

    if create == 'o':
        print("Création de la base de données")
        db.mise_a_jour_bd(conn, "data/create_table_projet.sql")
        db.mise_a_jour_trigger(conn, "data/create_trigger.sql")
        init=input("Souhaitez-vous insérer des valeurs de départ (o/n) ? ")
        while init != 'o' and init != 'n':
            init = input("Souhaitez-vous insérer des valeurs de départ (o/n) ? ")
        if init == 'o':
            db.mise_a_jour_bd(conn, "data/inserts_ok_projet.sql")

    input("\nAppuyez sur Entrée pour continuer")

    choice=1
    while choice != 0:
        while True:
            os.system('cls' if os.name=='nt' else 'clear')
            choice=int(input("Que souhaitez-vous faire ?\n"
                            "   Voir une table : 1\n"
                            "   Remplir une table : 2\n"
                            "   Vider une table : 3\n"
                            "   Saisie de requête au clavier : 4\n"
                            "   Simulation gestion client : 5\n"
                            "   Simulation gestion employeur : 6\n"
                            "   Quitter : 0\n"  
                            "Votre choix : "))
            if choice in (0, 1 ,2 ,3 ,4 ,5 ,6):
                break
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice==1:
            # GESTION MENU 1 : VISUALISATION DE TABLES
            m1.menu1(conn)
        elif choice==2:
            # GESTION MENU 2 : INSERT
            m2.menu2(conn)
        elif choice==3:
            # GESTION MENU 3: DELETE
            m3.menu3(conn)
        elif choice==4:
            # GESTION MENU 4 : SAISIE DE REQUETE AU CLAVIER
            m4.menu4(conn)
        elif choice==5:
            # GESTION MENU 5 : UTILISATION CLIENT
            m5.menu5(conn)
        elif choice==6:
            # GESTION MENU 6 : UTILISATION EMPLOYEUR
            m6.menu6(conn)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nMerci pour votre temps !")
            save=input("Voulez-vous sauvegarder les données (o/n) ? ")
            while save != 'o' and save != 'n':
                save = input("Voulez-vous sauvegarder les données (o/n) ? ")
            if save == 'o':
                conn.commit()
                print("Sauvegarde des données effectuée\n")
            print("A bientôt !")


if __name__ == "__main__":
    main()
