-- Create a store procedure `ComputeAverageScoreForUser`
--  that computes and stores the average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id int
)
BEGIN
    DECLARE total_score int;
    DECLARE no_of_corrections int;
    DECLARE average_score DECIMAL(10, 2);

    -- Calculate the user's total score
    SELECT SUM(score)
    INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the number of corrections
    SELECT COUNT(user_id)
    INTO no_of_corrections
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average score
    IF no_of_corrections > 0 THEN
        SET average_score = total_score / no_of_corrections;
    ELSE
        SET average_score = 0;
    END IF;

    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //

DELIMITER ;
