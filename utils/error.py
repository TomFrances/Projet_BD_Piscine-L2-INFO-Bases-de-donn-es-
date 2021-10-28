
def gestion_erreur_insert(table, list):
    print("\nErreur de l'insertion dans la table", "'", table, "' :")
    if list[0]=="CHECK constraint failed":
        attr=list[1].split('_', 2)
        if attr[2]=="age_client" or attr[2]=="capacite_max" or attr[2]=="tarif_interne" or attr[2]=="tarif_externe" or attr[2]=="revenu_horaire":
            print("L'attribut", '"', attr[2], '"',"doit être positif.")
        elif attr[2]=="statut_client":
            print("L'attribut", '"', attr[2], '"',"doit être 'interne' ou 'externe'.")
        elif attr[2]=="diplome":
            print("L'attribut", '"', attr[2], '"',"doit être 'BNSSA' ou 'BPJEPS'.")
        elif attr[2]=="nom_activite":
            print("L'attribut", '"', attr[2], '"',"doit être 'nage libre', 'cours particulier', 'aquagym' ou 'aquabike'.")
        elif attr[2]=="heure_debut_fin":
            print("L'heure de fin de l'activité doit être supérieure à l'heure de début.")
    elif list[0]=="NOT NULL constraint failed":
        attr=list[1].split('.')
        print("Vous devez renseigner la valeur de l'attribut", "'", attr[1], "'")
    elif list[0]=="UNIQUE constraint failed":
        attr=list[1].split('.')
        print("La valeur de l'attribut", '"', attr[1], '"', "est déjà utilisée.")
    elif list[0]=="FOREIGN KEY constraint failed":
        if table=='Creneaux':
            print("L'attribut 'Numéro activité' renseigné n'existe pas dans la table 'Activites' (erreur clé étrangère).")
        elif table=='Reservations':
            print("L'un des attributs 'Numéro client' ou 'Numéro créneau' renseigné n'est pas référencé dans la table 'Clients' ou 'Activites' (erreur clé étrangère).")
        elif table=='Surveillances':
            print("L'un des attributs 'Numéro maitre nageur' ou 'Numéro créneau' renseigné n'est pas référencé dans la table 'MaitreNageurs_base' ou 'Creneaux' (erreur clé étrangère).")
    else: # erreur des triggers
        print(list[0])
    print("\n")

def gestion_erreur_delete(table, list):
    print("\nEchec de la suppression dans la table", "'", table, "' :")
    if list[0]=="FOREIGN KEY constraint failed":
        print("Impossible de supprimer cette donnée de la table", table, ": elle est référencée dans une autre table.")
    print("\n")