
DROP VIEW IF EXISTS MaitreNageurs;
DROP VIEW IF EXISTS view_TarifsClients;

DROP TABLE IF EXISTS Surveillances;
DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS Creneaux;
DROP TABLE IF EXISTS Activites;
DROP TABLE IF EXISTS MaitreNageurs_base;
DROP TABLE IF EXISTS Clients;

--PRAGMA FOREIGN_KEYS=ON;

CREATE TABLE Clients (
	num_client INTEGER,
	nom_client TEXT NOT NULL,
	prenom_client TEXT NOT NULL,
	statut TEXT NOT NULL,
	age_client INTEGER NOT NULL,
	CONSTRAINT pk_clients_num_client PRIMARY KEY (num_client),
	CONSTRAINT ck_clients_age_client CHECK (age_client > 0),
	CONSTRAINT ck_clients_statut_client CHECK (statut IN ('interne', 'externe'))
);

CREATE TABLE MaitreNageurs_base (
	num_maitrenageur INTEGER,
	nom_maitrenageur TEXT NOT NULL,
	prenom_maitrenageur TEXT NOT NULL,
	adresse_maitrenageur TEXT NOT NULL,
	diplome TEXT NOT NULL,
	CONSTRAINT pk_maitrenageur_num_maitrenageur PRIMARY KEY (num_maitrenageur),
	CONSTRAINT ck_maitrenageur_diplome CHECK (diplome IN ('BNSSA', 'BPJEPS'))
);

CREATE TABLE Activites (
	num_activite INTEGER,
	nom_activite TEXT NOT NULL,
	capacite_max INTEGER NOT NULL,
	surveillable_bnssa BOOLEAN NOT NULL,
	tarif_interne INTEGER NOT NULL,
	tarif_externe INTEGER NOT NULL,
	revenu_horaire INTEGER NOT NULL,
	CONSTRAINT pk_activites_num_activite PRIMARY KEY (num_activite),
	CONSTRAINT ck_activites_nom_activite CHECK (nom_activite IN ('nage libre', 'cours particulier', 'aquagym', 'aquabike')),
	CONSTRAINT ck_activites_capacite_max CHECK (capacite_max > 0),
	CONSTRAINT ck_activites_tarif_interne CHECK (tarif_interne > 0),
	CONSTRAINT ck_activites_tarif_externe CHECK (tarif_externe > 0),
	CONSTRAINT ck_activites_revenu_horaire CHECK (revenu_horaire > 0)
);

CREATE TABLE Creneaux (
	num_creneau INTEGER,
	date_creneau DATE NOT NULL,
	heure_debut DATETIME NOT NULL,
	heure_fin DATETIME NOT NULL,
	num_activite INTEGER NOT NULL,
	CONSTRAINT pk_creneaux_num_creneau PRIMARY KEY (num_creneau),
	CONSTRAINT fk_creneaux_num_activite FOREIGN KEY (num_activite) REFERENCES Activites(num_activite),
	CONSTRAINT ck_creneaux_heure_debut_fin CHECK (heure_debut < heure_fin),
	CONSTRAINT ck_creneaux_heure_debut CHECK (strftime('%d',date_creneau) = strftime('%d', heure_debut)),
	CONSTRAINT ck_creneaux_heure_fin CHECK (strftime('%d',date_creneau) = strftime('%d', heure_fin))
);

CREATE TABLE Reservations (
	num_client INTEGER,
	num_creneau INTEGER,
	groupe INTEGER NOT NULL,
	CONSTRAINT pk_reservations_num_client_creneau PRIMARY KEY (num_client, num_creneau),
	CONSTRAINT fk_reservations_num_creneau FOREIGN KEY (num_creneau) REFERENCES Creneaux(num_creneau),
	CONSTRAINT fk_reservations_num_client FOREIGN KEY (num_client) REFERENCES Clients(num_client)
);

CREATE TABLE Surveillances (
	num_maitrenageur INTEGER,
	num_creneau INTEGER,
	CONSTRAINT pk_surveillances_num_maitrenageur_creneau PRIMARY KEY (num_maitrenageur, num_creneau),
	CONSTRAINT fk_surveillances_num_maitrenageur FOREIGN KEY (num_maitrenageur) REFERENCES MaitreNageurs_base(num_maitrenageur),
	CONSTRAINT fk_surveillances_num_creneau FOREIGN KEY (num_creneau) REFERENCES Creneaux(num_creneau)
);

CREATE VIEW MaitreNageurs (NumeroMaitreNageur, Nom, Prenom, Adresse, Diplome, Salaire) AS 
SELECT num_maitrenageur, nom_maitrenageur, prenom_maitrenageur, adresse_maitrenageur, diplome, 
	   SUM(round((julianday(heure_fin) - julianday(heure_debut))*24)*revenu_horaire)
FROM Surveillances 	JOIN Creneaux USING(num_creneau) 
					JOIN Activites USING(num_activite) 
					JOIN MaitreNageurs_base USING(num_maitrenageur)
GROUP BY num_maitrenageur
UNION
SELECT num_maitrenageur, nom_maitrenageur, prenom_maitrenageur, adresse_maitrenageur, diplome, 0
FROM MaitreNageurs_base
WHERE num_maitrenageur NOT IN (SELECT num_maitrenageur FROM Surveillances);

CREATE VIEW view_TarifsClients (NumeroClient, Nom, Prenom, Statut, Creneau, NumeroActivite, Activite, Tarif) AS
SELECT num_client, nom_client, prenom_client, statut, num_creneau, num_activite, nom_activite,
		CASE 
			WHEN (statut='interne') 	
				THEN 
					(SELECT tarif_interne FROM Activites A2 WHERE A1.num_activite=A2.num_activite)
				ELSE 
					(SELECT tarif_externe FROM Activites A2 WHERE A1.num_activite=A2.num_activite)
			END
FROM Activites A1 JOIN Creneaux USING(num_activite) JOIN Reservations USING(num_creneau) JOIN Clients USING(num_client);


