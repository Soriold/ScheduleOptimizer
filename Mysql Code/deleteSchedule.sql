USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `deleteSchedule` (IN username VARCHAR(20), IN scheduleID int)
BEGIN
	DELETE FROM FavoritedSchedule
    WHERE FavoritedSchedule.id = scheduleID AND FavoritedSchedule.StudentUsername = username;
END