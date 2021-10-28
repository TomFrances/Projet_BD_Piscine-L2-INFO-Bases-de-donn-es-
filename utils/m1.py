import os

def liste_clients(conn):
    """
    Affiche la liste de tous les clients.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Clients")

    rows = cur.fetchall()
    print("\nTable Clients\n"
          "num_client, nom_client, prenom_client, statut, age_client\n")
    for row in rows:
        print(row)

# ----------------------------------------------------
def liste_maitrenageurs(conn):
    """
    Affiche la liste de tous les maitre-nageurs.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM MaitreNageurs")

    rows = cur.fetchall()
    print("\nTable MaitreNageurs\n"
          "num_maitrenageur, nom_maitrenageur, prenom_maitrenageur, adresse_maitrenageur, diplome, salaire\n")
    for row in rows:
        print(row)

# ----------------------------------------------------
def liste_activites(conn):
    """
    Affiche la liste de toute les activités.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Activites")

    rows = cur.fetchall()
    print("\nTable Activités\n"
          "num_activite, nom_activite, capacite_max, surveillable_bnssa (1 oui, 0 non), tarif_interne, tarif_externe, revenu_horaire\n")
    for row in rows:
        print(row)

# ----------------------------------------------------
def liste_creneaux(conn):
    """
    Affiche la liste de tous les créneaux.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Creneaux")

    rows = cur.fetchall()
    print("\nTable Créneaux\n"
          "num_creneau, date_creneau, heure_debut, heure_fin, num_activite\n")
    for row in rows:
        print(row)

# ----------------------------------------------------
def liste_reservations(conn):
    """
    Affiche la liste de toute les réservations.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Reservations")

    rows = cur.fetchall()
    print("\nTable Réservations\n"
          "num_client, num_creneau, groupe\n")
    for row in rows:
        print(row)

# ----------------------------------------------------
def liste_surveillance(conn):
    """
    Affiche la liste de toute les surveillances.

    :param conn: Connexion à la base de données
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Surveillances")

    rows = cur.fetchall()
    print("\nTable Surveillances\n"
          "num_maitrenageur, num_creneau\n")
    for row in rows:
        print(row)

# ----------------------------------------------------

def menu1(conn):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        choice = int(input("Quelle table souhaitez-vous visualiser ?\n"
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
    if choice==1:
        liste_clients(conn)
    elif choice==2:
        liste_maitrenageurs(conn)
    elif choice==3:
        liste_activites(conn)
    elif choice==4:
        liste_creneaux(conn)
    elif choice==5:
        liste_surveillance(conn)
    elif choice==6:
        liste_reservations(conn)

    input("\nAppuyez sur Entrée pour continuer")

