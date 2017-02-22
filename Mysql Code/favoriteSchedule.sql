USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `favoriteSchedule` (IN username varchar(20), IN scheduleID int)
BEGIN
	UPDATE FavoritedSchedule
    SET FavoritedSchedule.Flag = 1
    WHERE FavoritedSchedule.id = scheduleID AND FavoritedSchedule.StudentUsername = username;
END