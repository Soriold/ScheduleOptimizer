USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `getFavoritedSchedule` (IN studentUsername varchar(8))
BEGIN

	/*Ensure the input parameter is not null*/
    IF studentUsername IS NULL THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username input is null.';
    END IF; 

	/*Ensure student does exist in the database*/
	IF studentUsername NOT IN (SELECT Username FROM dbo.Student) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username does not exist in database.';
	END IF;
    
    /*Get all rows from Favorited Schedule and FavoritedScheduleClassList*/
    SELECT * FROM FavoritedSchedule
		WHERE (FavoritedSchedule.StudentUsername = studentUsername) AND (FavoritedSchedule.Flag = 1); 
	
END $$

DELIMITER ;