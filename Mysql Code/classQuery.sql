USE `dbo`;
DELIMITER $$

CREATE PROCEDURE `classQuery` 
	(IN courseNum VARCHAR(10),
     IN weekendWed int,
     IN profRating double)
BEGIN
	SELECT * FROM Section
    WHERE Section.CourseNum = courseNum;
END