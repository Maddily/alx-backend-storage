-- Create a stored procedure `AddBonus`
-- that adds a new correction for a student
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id int,
    IN project_name varchar(255),
    IN score int
)
BEGIN
    DECLARE project_id int;

    -- Check if project exists; if not, create it
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    IF project_id IS NULL THEN
        INSERT INTO projects (name)
        VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END //

DELIMITER ;
