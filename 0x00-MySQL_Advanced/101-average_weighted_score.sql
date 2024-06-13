-- Create a stored procedure that computes and stores
-- the average weighted score for all students
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done boolean DEFAULT FALSE;
    DECLARE user_id int;
    DECLARE weighted_sum float;
    DECLARE total_weight int;
    DECLARE average_weighted_score FLOAT;

    DECLARE cur CURSOR FOR
        SELECT DISTINCT user_id
        FROM corrections;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    fetch_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE fetch_loop;
        END IF;

        -- Calculate the user's weighted sum
        SELECT SUM(corrections.score * projects.weight)
        INTO weighted_sum
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the total weight
        SELECT SUM(projects.weight)
        INTO total_weight
        FROM projects
        JOIN corrections ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET average_weighted_score = weighted_sum / total_weight;
        ELSE
            SET average_weighted_score = 0;
        END IF;

        UPDATE users
        SET users.average_score = average_weighted_score
        WHERE users.id = user_id;
    END LOOP;
    CLOSE cur;
END //

DELIMITER ;
