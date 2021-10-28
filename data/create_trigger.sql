DROP TRIGGER IF EXISTS UPDATE_CRENEAUX_DISSOCIES;
--
DROP TRIGGER IF EXISTS INSERT_CRENEAUX_DISSOCIES;
--
DROP TRIGGER IF EXISTS UPDATE_RESERVATIONS_ENFANT_MOINS_DIX_ANS;
--
DROP TRIGGER IF EXISTS INSERT_RESERVATIONS_ENFANT_MOINS_DIX_ANS;
--
DROP TRIGGER IF EXISTS UPDATE_RESERVATIONS_CAPACITE_MAX;
--
DROP TRIGGER IF EXISTS INSERT_RESERVATIONS_CAPACITE_MAX;
--
DROP TRIGGER IF EXISTS UPDATE_SURVEILLANCE_BNSSA_IMPOSSIBLE;
--
DROP TRIGGER IF EXISTS INSERT_SURVEILLANCE_BNSSA_IMPOSSIBLE;
--


CREATE TRIGGER INSERT_SURVEILLANCE_BNSSA_IMPOSSIBLE
BEFORE INSERT ON Surveillances
BEGIN
	SELECT
		CASE
			WHEN NEW.num_maitrenageur IN (SELECT num_maitrenageur FROM MaitreNageurs_base WHERE diplome = 'BNSSA') 
				AND NEW.num_creneau IN (SELECT num_creneau FROM Creneaux JOIN Activites USING (num_activite) WHERE surveillable_bnssa = 0) 
				THEN 
					RAISE (ABORT, 'Un BNSSA ne peut pas surveiller cette activité')
		END;
END;
--
CREATE TRIGGER UPDATE_SURVEILLANCE_BNSSA_IMPOSSIBLE
BEFORE UPDATE ON Surveillances
BEGIN
	SELECT
		CASE
			WHEN NEW.num_maitrenageur IN (SELECT num_maitrenageur FROM MaitreNageurs_base WHERE diplome = 'BNSSA') 
				AND NEW.num_creneau IN (SELECT num_creneau FROM Creneaux JOIN Activites USING (num_activite) WHERE surveillable_bnssa = 0) 
				THEN 
					RAISE (ABORT, 'Un BNSSA ne peut pas surveiller cette activité')
		END;
END;
--
CREATE TRIGGER INSERT_RESERVATIONS_CAPACITE_MAX
BEFORE INSERT ON Reservations
BEGIN
	SELECT
		CASE
			WHEN (	SELECT COUNT(num_client) AS nb_res 
					FROM Reservations 
					WHERE num_creneau=NEW.num_creneau 
					GROUP BY num_creneau) >= (	SELECT capacite_max 
												FROM Activites A JOIN Creneaux C ON (A.num_activite=C.num_activite AND C.num_creneau=NEW.num_creneau))
			THEN 
				RAISE (ABORT, 'Ce créneau est plein')
		END;
END;
--
CREATE TRIGGER UPDATE_RESERVATIONS_CAPACITE_MAX
BEFORE UPDATE ON Reservations
BEGIN
	SELECT
		CASE
			WHEN (	SELECT COUNT(num_client) AS nb_res 
					FROM Reservations 
					WHERE num_creneau=NEW.num_creneau 
					GROUP BY num_creneau) >= (	SELECT capacite_max 
												FROM Activites A JOIN Creneaux C ON (A.num_activite=C.num_activite AND C.num_creneau=NEW.num_creneau))
			THEN 
				RAISE (ABORT, 'Ce créneau est plein')
		END;
END;
--
CREATE TRIGGER INSERT_RESERVATIONS_ENFANT_MOINS_DIX_ANS
BEFORE INSERT ON Reservations
BEGIN
	SELECT
		CASE
            WHEN   (SELECT age_client
					FROM Clients
					WHERE num_client=NEW.num_client) < 10
					AND	NOT EXISTS (SELECT R.num_client
									FROM Reservations R JOIN Clients C ON (R.num_client=C.num_client AND num_creneau=NEW.num_creneau AND groupe=NEW.groupe AND age_client >= 18))
            THEN 
                RAISE (ABORT, 'Ce client doit être accompagné par une personne majeure')
        END;
END;
--
CREATE TRIGGER UPDATE_RESERVATIONS_ENFANT_MOINS_DIX_ANS
BEFORE UPDATE ON Reservations
BEGIN
	SELECT
		CASE
            WHEN (SELECT age_client
				  FROM Clients
				  WHERE num_client=NEW.num_client) < 10
				  AND NOT EXISTS (SELECT R.num_client
								  FROM Reservations R JOIN Clients C ON (R.num_client=C.num_client AND num_creneau=NEW.num_creneau AND groupe=NEW.groupe AND age_client >= 18))
            THEN 
                RAISE (ABORT, 'Ce client doit être accompagné par une personne majeure')
        END;
END;
--
CREATE TRIGGER INSERT_CRENEAUX_DISSOCIES
BEFORE INSERT ON Creneaux
BEGIN
	SELECT
		CASE
			WHEN EXISTS (SELECT num_creneau
						 FROM Creneaux
						 WHERE date_creneau=NEW.date_creneau AND ((NEW.heure_debut>heure_debut AND NEW.heure_debut<heure_fin)
																   OR (NEW.heure_fin>heure_debut AND NEW.heure_debut<heure_fin)
																   OR (NEW.heure_debut<heure_debut AND NEW.heure_fin>heure_fin)))
			THEN
				RAISE(ABORT, 'Ce créneau empiète sur un autre')
		END;
END;
--
CREATE TRIGGER UPDATE_CRENEAUX_DISSOCIES
BEFORE UPDATE ON Creneaux
BEGIN
	SELECT
		CASE
			WHEN EXISTS (SELECT num_creneau
						 FROM Creneaux
						 WHERE date_creneau=NEW.date_creneau AND ((NEW.heure_debut>heure_debut AND NEW.heure_debut<heure_fin)
															       OR (NEW.heure_fin>heure_debut AND NEW.heure_debut<heure_fin)
																   OR (NEW.heure_debut<heure_debut AND NEW.heure_fin>heure_fin)))
			THEN
				RAISE(ABORT, 'Ce créneau empiète sur un autre')
		END;
END;
