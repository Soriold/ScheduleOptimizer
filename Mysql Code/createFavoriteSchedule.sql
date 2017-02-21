USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `createFavoritedSchedule` 
	(IN username varchar(8), 
	IN crn1 smallint, 
    IN crn2 smallint, 
    IN crn3 smallint, 
    IN crn4 smallint, 
    IN crn5 smallint,
    IN crn6 smallint
	OUT scheduleID int)
BEGIN
	/*Ensure the input parameter is not null*/
    IF username IS NULL THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username input is null.';
    END IF; 
    
    /*Ensure the input parameter is not null*/
    IF crn1 IS NULL THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Need to give at least one class.';
    END IF; 
    
	/*Ensure student does exist in the database*/
	IF username NOT IN (SELECT Username FROM dbo.Student) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username does not exist in database.';
	END IF;
    
    BEGIN
		INSERT INTO FavoritedSchedule (Flag, StudentUsername) VALUES (0, username);
        
        IF crn1 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn1);
		END IF;
        
        IF crn2 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn2);
		END IF;
        
        IF crn3 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn3);
		END IF;
        
        IF crn4 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn4);
		END IF;
        
        IF crn5 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn5);
		END IF;
        
        IF crn6 <> 0 THEN
			INSERT INTO FavoritedScheduleClassList (id, CRN) VALUES (LAST_INSERT_ID(), crn6);
		END IF;
		
		SET scheduleID = LAST_INSERT_ID();
        
	END;
END $$

DELIMITER ;
        