-- Jeux de données NOK 

-- Erreur : Client avec numéro existant
INSERT INTO Clients VALUES (17,'Erroné','Erroné','interne', 38);
-- Erreur : Nom absent (Un cinqième attribut est attendu)
INSERT INTO Clients VALUES (17,'Martin','interne', 27);
-- Erreur : Clients sans Nom 
INSERT INTO Clients VALUES (17,NULL,'Martin','interne', 27);
-- Erreur : Clients sans Prenom 
INSERT INTO Clients VALUES (17,'Keller',NULL,'interne', 27);
-- Erreur : Age négatif 
INSERT INTO Clients VALUES (17,'Keller','Martin','interne', -1);
-- Erreur : statut non défini
INSERT INTO Clients VALUES (17,'Keller','Martin','exterieur', 27);

-- Erreur : Diplome non défini 
INSERT INTO MaitreNageurs_Base VALUES (103,'Durroux','Michel','Rue Kleber','BSB');
-- Erreur : MaitreNageur sans adresse  
INSERT INTO MaitreNageurs_Base VALUES (103,'Durroux','Michel',NULL,'BNSSA');

-- Erreur : Activite existante
INSERT INTO Activites VALUES (2,'aquabike',15,0,20,25,15);
-- Erreur : Nom activité non défini 
INSERT INTO Activites VALUES (6,'cours individuel',1,0,30,35,20);
-- Erreur : Revenu horaire négatif 
INSERT INTO Activites VALUES (5,'nage libre',10,0,10,15,-10);
-- Erreur : Capacité max nulle 
INSERT INTO Activites VALUES (5,'nage libre',0,1,10,15,50);

-- Erreur : Les Trois dates doivent etres les memes pour un meme créneau (DATE(date_creneau)=DATE(heure_debut)=DATE(heure_fin))
INSERT INTO Creneaux VALUES (6,'2021-07-04','2021-07-03 18:30:00','2021-07-03 20:30:00', 5);
INSERT INTO Creneaux VALUES (6,'2021-07-03','2021-07-04 18:30:00','2021-07-03 20:30:00', 5);
-- Erreur : Ces creneaux empiètent sur un autre
INSERT INTO Creneaux VALUES (6,'2021-07-03','2021-07-03 18:25:00','2021-07-03 20:35:00', 5);
INSERT INTO Creneaux VALUES (6,'2021-07-03','2021-07-03 17:30:00','2021-07-03 19:30:00', 5);
INSERT INTO Creneaux VALUES (6,'2021-07-03','2021-07-03 20:00:00','2021-07-03 22:30:00', 5);
INSERT INTO Creneaux VALUES (6,'2021-07-03','2021-07-03 20:00:00','2021-07-03 20:10:00', 5);
-- Erreur : Creneau existant
INSERT INTO Creneaux VALUES (5,'2021-07-04','2021-07-04 12:30:00','2021-07-04 14:30:00', 5);

-- Erreur : Capacité max atteinte
INSERT INTO Reservations VALUES (12,5,7);
-- Erreur : Impossible de réserver seul(e) (doit etre accompagné(e) d'une personne majeure)
INSERT INTO Reservations VALUES (17,2,7);
-- Erreur : Client inconnu 
INSERT INTO Reservations VALUES (20,4,1);
-- Erreur : Creneau inconnu 
INSERT INTO Reservations VALUES (15,6,5);
-- Erreur : Créneau non défini (clé étrangère inconnue)
INSERT INTO Reservations VALUES (18,6,6);

-- Erreur : Activité non surveillable par un BNSSA
INSERT INTO Surveillances VALUES (100, 2);
-- Erreur : Numero MaitreNageur n'existe pas dans MaitreNageurs
INSERT INTO Surveillances VALUES (111, 5);