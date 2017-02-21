USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `getClassList` (IN scheduleID int)
BEGIN
/*Ensure the input parameter is not null*/
    IF scheduleID IS NULL THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Schedule ID input is null.';
    END IF; 

	/*Ensure student does exist in the database*/
	IF scheduleID NOT IN (SELECT id FROM dbo.FavoritedSchedule) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username does not exist in database.';
	END IF;
    
    /*Get all rows from Favorited Schedule and FavoritedScheduleClassList*/
    SELECT * FROM FavoritedScheduleClassList
		WHERE FavoritedScheduleClassList.id = scheduleID; 
END $$

DELIMITER ;