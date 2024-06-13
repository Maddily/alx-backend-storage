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
    INSERT IGNORE INTO projects (name) VALUES (project_name);
    SELECT id INTO project_id FROM projects WHERE name = project_name LIMIT 1;
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END //

DELIMITER ;
