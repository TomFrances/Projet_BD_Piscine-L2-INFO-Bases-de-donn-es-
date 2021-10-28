import os
import sqlite3
from utils import error, m1


# ----------------------------------------------------
def delete_clients(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table Clients.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_clients(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_client, "
            "nom_client, prenom_client, statut ou age_client) : "))
            if attr in ("num_client", "nom_client", "prenom_client", "statut", "age_client"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM Clients WHERE "+attr+op+'?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('Clients', erreur)

        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def delete_maitrenageurs(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table MaitreNageurs_base.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_maitrenageurs(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_maitrenageur, "
            "nom_maitrenageur, prenom_maitrenageur, adresse_maitrenageur ou diplome) : "))
            if attr in ("num_maitrenageur", "nom_maitrenageur", "prenom_maitrenageur", "adresse_maitrenageur", "diplome"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM MaitreNageurs_base WHERE " + attr + op + '?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('MaitreNageurs_base', erreur)

        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def delete_activites(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table Activites.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_activites(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_activite, nom_activite, "
            "capacite_max, surveillable_bnssa, tarif_interne, tarif_externe ou revenu_horaire) : "))
            if attr in ("num_activite", "nom_activite", "surveillable_bnssa", "capacite_max", "tarif_externe", "tarif_interne", "revenu_horaire"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM Activites WHERE " + attr + op + '?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('Activites', erreur)

        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def delete_creneaux(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table Creneaux.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_activites(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_creneau, "
            "date_creneau, heure_debut, heure_fin ou num_activite) : "))
            if attr in ("num_creneau", "date_creneau", "heure_debut", "heure_fin", "num_activite"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM Creneaux WHERE " + attr + op + '?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('Creneaux', erreur)

        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

def delete_surveillances(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table Surveillances.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_surveillance(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_maitrenageur, num_creneau) : "))
            if attr in ("num_maitrenageur", "num_creneau"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM Surveillances WHERE " + attr + op + '?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('Surveillances', erreur)
        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

def delete_reservations(conn):
    """
        Supprime une ou plusieurs ligne(s) dans la table Reservations.

        :param conn: Connexion à la base de données
        """
    cntn = 'y'
    while cntn != 'n':
        m1.liste_reservations(conn)
        while True:
            attr = str(input("\nChoix de l'attribut de la condition (num_client, num_creneau) : "))
            if attr in ("num_client", "num_creneau"):
                break
        while True:
            op = str(input("Choix de la comparaison ( <, >, <=, >=, = ou != ) : "))
            if op in ('<', '>', '=', '!=', '<=', '>='):
                break
        val = input("Choix de la valeur : ")
        cur = conn.cursor()
        sql = "DELETE FROM Reservations WHERE " + attr + op + '?'
        try:
            cur.execute(sql, (val,))
            print("\nSuppression effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_delete('Reservations', erreur)

        while True:
            cntn = str(input("Souhaitez-vous supprimer une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break


def menu3(conn):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        choice = int(input("Dans quelle table souhaitez-vous supprimer des données ?\n"
                           "  Les clients : 1\n"
                           "  Les maitre-nageurs : 2\n"
                           "  Les activités : 3\n"
                           "  Les créneaux : 4\n"
                           "  Les surveillances : 5\n"
                           "  Les resérvations : 6\n"
                           "Votre choix : "))
        if choice in (0, 1, 2, 3, 4, 5, 6):
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    if choice == 1:
        delete_clients(conn)
    elif choice == 2:
        delete_maitrenageurs(conn)
    elif choice == 3:
        delete_activites(conn)
    elif choice == 4:
        delete_creneaux(conn)
    elif choice == 5:
        delete_surveillances(conn)
    elif choice == 6:
        delete_reservations(conn)

    input("\nAppuyez sur Entrée pour continuer ")
