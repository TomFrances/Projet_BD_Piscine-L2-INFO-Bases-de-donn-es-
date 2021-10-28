import os
import sqlite3
from utils import error, db, m2

def menu5(conn):
    choice = 1
    while choice != 0:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            choice = int(input("Que souhaitez-vous faire :\n"
                               "    Vous enregistrer comme nouveau client : 1\n"
                               "    Regarder les créneaux disponibles : 2\n"
                               "    Connaitre le tarif des activités : 3\n"
                               "    Réserver un créneau : 4\n"
                               "    Regarder vos réservations : 5\n"
                               "    Annuler une réservation : 6\n"
                               "    Modifier ses informations personnelles : 7\n"
                               "    Quitter : 0\n"
                               "Votre choix : "))
            if choice in (0, 1, 2, 3, 4, 5, 6, 7):
                break
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == 1:
            m2.insert_clients(conn)
        elif choice == 2:
            while True:
                res = int(input("Souhaitez-vous regarder les créneaux d'une date ou d'une activité en particulier ?\n"
                                "   Date : 1\n"
                                "   Activité : 2\n"
                                "Votre choix : "))
                if res in (1, 2):
                    break
            if res == 1:
                date = str(input("Choix de la date (format YYYY-MM-DD) : "))
                sql = """   SELECT num_creneau, heure_debut, heure_fin, nom_activite 
                            FROM Creneaux JOIN Activites USING(num_activite) 
                            WHERE num_creneau IN (  SELECT num_creneau
                                                    FROM Creneaux NATURAL JOIN Reservations NATURAL JOIN Activites
                                                    WHERE date_creneau = ?
                                                    GROUP BY num_creneau
                                                    HAVING COUNT(num_client) < capacite_max 
                                                    UNION
                                                    SELECT num_creneau
                                                    FROM Creneaux
                                                    WHERE date_creneau = ? 
                                                    AND num_creneau NOT IN (SELECT num_creneau
                                                                            FROM Reservations) ) """
                data = [date, date]
                cur = conn.cursor()
                cur.execute(sql, data)
                rows = cur.fetchall()
                print("\nListe des créneaux du ", date, ": ")
                for row in rows:
                    print(row)
            elif res == 2:
                while True:
                    act = str(input("Choix de l'activité (nage libre, cours particulier, aquagym ou aquabike) : "))
                    if act in ("nage libre", "cours particulier", "aquagym", "aquabike"):
                        break
                sql = """   SELECT num_creneau, heure_debut, heure_fin, nom_activite 
                            FROM Creneaux JOIN Activites USING(num_activite) 
                            WHERE num_creneau IN (  SELECT num_creneau
                                                    FROM Creneaux NATURAL JOIN Reservations NATURAL JOIN Activites
                                                    WHERE nom_activite = ?
                                                    GROUP BY num_creneau
                                                    HAVING COUNT(num_client) < capacite_max 
                                                    UNION
                                                    SELECT num_creneau
                                                    FROM Creneaux
                                                    WHERE nom_activite = ?
                                                    AND num_creneau NOT IN (SELECT num_creneau
                                                                            FROM Reservations) ) """
                data = [act, act]
                cur = conn.cursor()
                cur.execute(sql, data)
                rows = cur.fetchall()
                print("\nListe des créneaux de l'activité", act, ": ")
                for row in rows:
                    print(row)
        elif choice == 3:
            cur = conn.cursor()
            id_client = int(input("Veuillez renseigner votre numéro de client : "))
            cur.execute("SELECT statut FROM Clients WHERE num_client = ?", (id_client,))
            try:
                statut = cur.fetchone()[0]
            except:
                print("Vous avez renseigné un numéro de client inconnu.\n")
            if statut == "externe":
                cur.execute("SELECT num_activite, nom_activite, tarif_externe FROM Activites")
            else:
                cur.execute("SELECT num_activite, nom_activite, tarif_interne FROM Activites")
            rows = cur.fetchall()
            print("\nListe des tarifs '", statut, "' : ")
            for row in rows:
                print(row)
        elif choice == 4:
            cur = conn.cursor()
            # suppression des triggers, conflit avec la gestion applicative de la contrainte
            cur.execute("DROP TRIGGER IF EXISTS INSERT_RESERVATIONS_ENFANT_MOINS_DIX_ANS")
            cur.execute("DROP TRIGGER IF EXISTS UPDATE_RESERVATIONS_ENFANT_MOINS_DIX_ANS")

            id_creneau = int(input("Quel créneau souhaitez-vous réserver : "))
            nb_res = int(input("Combien de places souhaitez-vous réserver : "))

            # récupération du numéro de groupe
            cur.execute("SELECT MAX(groupe) FROM Reservations")
            groupe = cur.fetchone()[0] + 1

            # nombre de places restantes pour un creneau
            cur.execute("SELECT capacite_max - COUNT(*)"
                        "FROM Reservations JOIN Creneaux USING(num_creneau) JOIN Activites USING(num_activite) "
                        "WHERE num_creneau = ? ", (id_creneau,))
            nb_places_rest = cur.fetchone()[0]

            if nb_res > nb_places_rest:
                print("Il ne reste pas assez de places sur ce créneau.\n")
            else:
                data = []
                adulte_present = False
                dix_ans_present = False
                while nb_res > 0:
                    id_client = int(input("Numéro de client à ajouter à la réservation : "))
                    l = [id_client, id_creneau, groupe]
                    data.append(l)
                    cur.execute("SELECT age_client FROM Clients WHERE num_client = ?", (id_client,))
                    try:
                        age = cur.fetchone()[0]
                        if age <= 10:
                            dix_ans_present = True
                        elif age >= 18:
                            adulte_present = True
                    except TypeError:
                        print("Atention, ce numéro de client est inconnu\n")
                    nb_res = nb_res - 1
                if dix_ans_present and not adulte_present:
                    print("Réservation impossible : un enfant de 10 ans ou moins doit être accompagné par un adulte\n")
                else:
                    for d in data:
                        try:
                            cur.execute("INSERT INTO Reservations VALUES (?,?,?)", d)
                        except sqlite3.IntegrityError as err:
                            erreur = str(err).split(': ')
                            error.gestion_erreur_insert('Reservations', erreur)
        elif choice == 5:
            id_client = int(input("Veuillez renseigner votre numéro de client : "))
            sql = """   SELECT num_creneau, date_creneau, heure_debut, heure_fin, nom_activite
                        FROM Reservations JOIN Creneaux USING(num_creneau) JOIN Activites USING(num_activite)
                        WHERE num_client = ?    """
            print("Voici vos réservations actuelles :")
            cur = conn.cursor()
            cur.execute(sql, (id_client,))
            rows = cur.fetchall()
            for row in rows:
                print(row)
        elif choice == 6:
            print("L'annulation d'une réservation supprimera également les réservations des clients faisait partie du même groupe que vous, sur le même créneau.\n")
            id_client = int(input("Veuillez renseigner votre numéro de client : "))
            id_creneau = int(input("Veuillez renseigner le numéro de créneau que vous souhaitez supprimer : "))
            sql = "SELECT groupe FROM Reservations WHERE num_client = ? AND num_creneau = ?"
            data = [id_client, id_creneau]
            cur = conn.cursor()
            cur.execute(sql, data)
            groupe = cur.fetchone()[0]
            sql = "DELETE FROM Reservations WHERE num_creneau = ? AND groupe = ?"
            data = [id_creneau, groupe]
            try:
                cur.execute(sql, data)
                print("Votre réservation a été annulée.\n")
            except:
                print("Echec de l'annulation de la réservation.\n")
        elif choice == 7:
            id_client = int(input("Veuillez renseigner votre numéro de client : "))
            new_nom = str(input("Nouveau nom : "))
            new_prenom = str(input("Nouveau prénom : "))
            while True:
                new_statut = str(input("Nouveau statut (externe ou interne) : "))
                if new_statut == 'externe' or new_statut == 'interne':
                    break
            new_age = int(input("Nouvel age : "))
            data = (None if new_nom == '' else new_nom, None if new_prenom == '' else new_prenom, new_statut, new_age, id_client)
            cur = conn.cursor()
            try:
                cur.execute("UPDATE Clients SET nom_client = ?, prenom_client = ?, statut = ?, age_client = ? WHERE num_client = ?", data)
                print("Modification effectuée avec succès.\n")
            except sqlite3.IntegrityError as err:
                erreur = str(err).split(': ')
                error.gestion_erreur_insert('Clients', erreur)

        # restoration des triggers
        db.mise_a_jour_trigger(conn, "data/create_trigger.sql")
        input("\nAppuyez sur Entrée pour continuer")