import os
import sqlite3
from utils import error, db

def menu6(conn):
    choice = 1
    while choice != 0:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            choice = int(input("Que souhaitez-vous faire :\n"
                               "    Voir la recette du jour : 1\n"
                               "    Voir les activités les plus réservées (proportions) : 2\n"
                               "    Voir les statistiques suivant le statut des clients (répartitions de la clientèle, des réservations et des gains totaux) : 3\n"
                               "    Voir les salaires : 4\n"
                               "    Quitter : 0\n"
                               "Votre choix : "))
            if choice in (0, 1, 2, 3, 4):
                break
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == 1:
            date = str(input("Choix de la date (format YYYY-MM-DD) : "))
            data = [date, date]
            sql = """   WITH GainsExternes AS ( SELECT date_creneau AS date, SUM(tarif_externe) AS gainE
                                                FROM Clients Cl
                                                JOIN Reservations R ON (Cl.num_client=R.num_client AND date_creneau = ?) 
                                                JOIN Creneaux Cr USING(num_creneau) 
                                                JOIN Activites A ON (A.num_activite=Cr.num_activite AND statut='externe')
                                                GROUP BY date_creneau),
                        GainsInternes AS (  SELECT date_creneau AS date, SUM(tarif_interne) AS gainI
                                            FROM Clients Cl
                                            JOIN Reservations R ON (Cl.num_client=R.num_client AND date_creneau = ?) 
                                            JOIN Creneaux Cr USING(num_creneau) 
                                            JOIN Activites A ON (A.num_activite=Cr.num_activite AND statut='interne')
                                            GROUP BY date_creneau)
                        SELECT gainE + gainI
                        FROM GainsExternes JOIN GainsInternes USING(date) """
            cur = conn.cursor()
            cur.execute(sql, data)
            r = cur.fetchone()[0]
            print("\nRecette du", date, ":", r, "euros\n")
        elif choice == 2:
            sql = """   WITH nbResAct AS (  SELECT nom_activite, COUNT(num_client) AS nbRes
                                            FROM Reservations NATURAL JOIN Creneaux NATURAL JOIN Activites
                                            GROUP BY nom_activite ),
                            capaTotale AS ( SELECT nom_activite, SUM(capacite_max) as capaTot
                                            FROM Creneaux NATURAL JOIN Activites
                                            GROUP BY nom_activite )
                        SELECT nom_activite, ROUND(nbRes * 100.0 / capaTot) AS prop
                        FROM nbResAct NATURAL JOIN capaTotale 
                        ORDER BY prop DESC """
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            print("\nActivités et proportions de réservations par rapport à leur capacité max (%) : ")
            for row in rows:
                print(row)
        elif choice == 3:
            sqlClients = """ WITH nbClientsStatut AS (  SELECT statut, COUNT(num_client) AS nbClients
                                                        FROM Clients
                                                        GROUP BY statut ),
                                nbClientsTotal AS ( SELECT COUNT(*) AS total
                                                    FROM Clients )
                                SELECT statut, nbClients, ROUND(nbClients * 100.0 / total) as prop
                                FROM nbClientsStatut, nbClientsTotal
                                ORDER BY prop DESC """
            cur = conn.cursor()
            cur.execute(sqlClients)
            rows = cur.fetchall()
            print("\nClients : \n"
                  "Statut, nombre, proportion (%)")
            for row in rows:
                print(row)
            sqlGains = """ WITH GainsStatut AS (SELECT statut, SUM(tarif_externe) AS gain
                                                FROM Clients
                                                NATURAL JOIN Reservations
                                                NATURAL JOIN Creneaux
                                                JOIN Activites ON (Activites.num_activite=Creneaux.num_activite AND statut='externe')
                                                GROUP BY statut
                                                UNION
                                                SELECT statut, SUM(tarif_interne) AS gain
                                                FROM Clients
                                                NATURAL JOIN Reservations
                                                NATURAL JOIN Creneaux
                                                JOIN Activites ON (Activites.num_activite=Creneaux.num_activite AND statut='interne')
                                                GROUP BY statut ),
                                GainsTotaux AS (SELECT SUM(gain) AS total
                                                FROM GainsStatut)
                                SELECT statut, gain, ROUND(gain * 100.0 / total) AS prop
                                FROM GainsStatut, GainsTotaux 
                                ORDER BY prop DESC """
            cur = conn.cursor()
            cur.execute(sqlGains)
            rows = cur.fetchall()
            print("\nGains : \n"
                  "Statut, revenu, proportion (%)")
            for row in rows:
                print(row)

            sqlFreq = """   WITH nbResStatut AS (   SELECT statut, COUNT(num_client) AS nbRes
                                                    FROM Reservations
                                                    NATURAL JOIN Clients  
                                                    GROUP BY statut ),
                                nbResTot AS (   SELECT SUM(nbRes) AS total
                                                FROM nbResStatut )
                                SELECT statut, nbRes, ROUND(nbRes * 100.0 / total) AS prop
                                FROM nbResStatut, nbResTot 
                                ORDER BY prop DESC """
            cur = conn.cursor()
            cur.execute(sqlFreq)
            rows = cur.fetchall()
            print("\nRéservations  : \n"
                  "Statut, nombre, proportion (%)")
            for row in rows:
                print(row)
        elif choice == 4:
            cur = conn.cursor()
            cur.execute(""" SELECT * FROM MaitreNageurs ORDER BY salaire DESC""")
            rows = cur.fetchall()
            print("\nTable MaitreNageurs\n"
                  "Numéro, Nom, Prénom, Adresse, Diplome, Salaire\n")
            for row in rows:
                print(row)

        input("\n\nAppuyez sur Entrée pour continuer")