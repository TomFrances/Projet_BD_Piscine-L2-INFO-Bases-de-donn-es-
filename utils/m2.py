import os
import sqlite3
from utils import error

def insert_clients(conn):
    """
    Insère une ligne dans la table Clients.

    :param conn: Connexion à la base de données
    """

    cntn = 'y'
    while cntn != 'n':
        num = int(input("Numéro : "))
        nom = str(input("Nom : "))
        prenom = str(input("Prénom : "))
        while True:
            statut = str(input("Statut (externe ou interne) : "))
            if statut in ("externe", "interne"):
                break
        age = int(input("Age : "))
        data = (num, None if nom == '' else nom, None if prenom == '' else prenom, statut, age)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Clients VALUES (?,?,?,?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('Clients', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def insert_maitrenageurs(conn):
    """
    Insère une ligne dans la table MaitreNageurs_base.

    :param conn: Connexion à la base de données
    """
    cntn = 'y'
    while cntn != 'n':
        num = int(input("Numéro : "))
        nom = str(input("Nom : "))
        prenom = str(input("Prénom : "))
        adresse = str(input("Adresse : "))
        while True:
            diplome = str(input("Diplôme (BNSSA ou BPJEPS) : "))
            if diplome in ("BNSSA", "BPJEPS"):
                break
        data = (num, None if nom == '' else nom, None if prenom == '' else prenom, None if adresse == '' else adresse, None if diplome == '' else diplome)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO MaitreNageurs_base VALUES (?,?,?,?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('MaitreNageurs_base', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def insert_activites(conn):
    """
    Insère une ligne dans la table Activités.

    :param conn: Connexion à la base de données
    """
    cntn = 'y'
    while cntn != 'n':
        num = int(input("Numéro : "))
        while True:
            nom = str(input("Nom (nage libre, cours particulier, aquabike ou aquagym) : "))
            if nom in ("nage libre", "cours particulier", "aquabike", "aquagym"):
                break
        capa = int(input("Capacité maximum : "))
        surv = int(input("Surveillable par un BNSSA (oui 1, 0 non) : "))
        tar_i = int(input("Tarif interne : "))
        tar_e = int(input("Tarif externe : "))
        rev = int(input("Revenu horaire : "))
        data = (num, None if nom == '' else nom, capa, surv if (surv == 1 or surv == 0) else 1, tar_i, tar_e, rev)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Activites VALUES (?,?,?,?,?,?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('Activites', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------
def insert_creneaux(conn):
    """
    Insère une ligne dans la table Créneaux.

    :param conn: Connexion à la base de données
    """
    cntn = 'y'
    while cntn != 'n':
        num = int(input("Numéro : "))
        date = str(input("Date du créneau (format YYYY-MM-DD) : "))
        h_d = str(input("Heure de début du créneau (format HH:MM:SS) : "))
        h_f = str(input("Heure de fin du créneau (format HH:MM:SS) :"))
        act = int(input("Numéro activité : "))
        data = (num, date, date+' '+h_d, date+' '+h_f, act)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Creneaux VALUES (?,?,?,?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('Creneaux', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------

def insert_surveillance(conn):
    """
    Insère une ligne dans la table Surveillances.

    :param conn: Connexion à la base de données
    """
    cntn = 'y'
    while cntn != 'n':
        maitrenageur = int(input("Numéro maitre-nageur: "))
        creneau = int(input("Numéro créneau : "))
        data = (maitrenageur, creneau)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Surveillances VALUES (?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('Surveillances', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------

def insert_reservations(conn):
    """
    Insère une ligne dans la table Réservations.

    :param conn: Connexion à la base de données
    """
    cntn = 'y'
    while cntn != 'n':
        client = int(input("Numéro client : "))
        creneau = int(input("Numéro créneau : "))
        groupe = int(input("Numéro groupe : "))
        data = (client, creneau, groupe)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Reservations VALUES (?,?,?)", data)
            print("Insertion effectuée avec succès.\n")
        except sqlite3.IntegrityError as err:
            erreur = str(err).split(': ')
            error.gestion_erreur_insert('Reservations', erreur)

        while True:
            cntn = str(input("Souhaitez-vous ajouter une autre valeur (y/n)"))
            if cntn == "y" or cntn == "n":
                break

# ----------------------------------------------------

def menu2(conn):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        choice=int(input("Dans quelle table souhaitez-vous ajouter des valeurs ?\n"
                         "  Les clients : 1\n"
                         "  Les maitre-nageurs : 2\n"
                         "  Les activités : 3\n"
                         "  Les créneaux : 4\n"
                         "  Les surveillances : 5\n"
                         "  Les resérvations : 6\n"
                         "  Quitter : 0\n"
                         "Votre choix : "))
        if choice in (0, 1, 2, 3, 4, 5, 6):
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    if choice == 1:
        insert_clients(conn)
    elif choice == 2:
        insert_maitrenageurs(conn)
    elif choice == 3:
        insert_activites(conn)
    elif choice == 4:
        insert_creneaux(conn)
    elif choice == 5:
        insert_surveillance(conn)
    elif choice == 6:
        insert_reservations(conn)

    input("\nAppuyez sur Entrée pour continuer ")