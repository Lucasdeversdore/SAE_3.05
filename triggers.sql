delimiter |
CREATE OR REPLACE verifMDP BEFORE INSERT OR UPDATE OF mdp ON CHIMISTE FOR EACH ROW DECLARE 
DECLARE
    invalid_password EXCEPTION;
BEGIN 
    -- Vérifie la présence d'une majuscule
    IF NOT REGEXP_LIKE(new.mdp, '[A-Z]') THEN
        RAISE invalid_password;
    END IF;

    -- Vérifie la présence d'un chiffre
    IF NOT REGEXP_LIKE(new.mdp, '[0-9]') THEN
        RAISE invalid_password;
    END IF;

    -- Vérifie la présence d'un caractère spécial
    IF NOT REGEXP_LIKE(new.mdp, '[^a-zA-Z0-9]') THEN
        RAISE invalid_password;
    END IF;

EXCEPTION
    WHEN invalid_password THEN
        RAISE_APPLICATION_ERROR(-20001, 'Le mot de passe doit contenir au moins une majuscule, un chiffre et un caractère spécial.');
END |
delimiter ;