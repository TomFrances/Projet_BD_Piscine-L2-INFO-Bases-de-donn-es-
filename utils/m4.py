import os
import sqlite3

def menu4(conn):
    os.system('cls' if os.name == 'nt' else 'clear')
    sql = str(input("Veuillez écrire la requête que vous souhaitez exécuter : \n"))
    try:
        cur = conn.cursor()
        cur.execute(sql)
        print("\nRequête effectuée avec succès.\n")
        rows = cur.fetchall()
        print("\nRésultat\n")
        for row in rows:
            print(row[0])
    except:
        print("Echec de la requête.\n")

    input("\nAppuyez sur Entrée pour continuer")
