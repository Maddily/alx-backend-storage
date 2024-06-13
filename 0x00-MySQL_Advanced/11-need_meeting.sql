-- Create a view that lists all students that have a score
-- under 80 and no last_meeting or more than 1 month
-- since the last meeting
CREATE VIEW need_meeting
AS SELECT name
FROM students
WHERE score < 80
AND (
    last_meeting is NULL
    OR last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH)
);
