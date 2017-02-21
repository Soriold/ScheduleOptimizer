CREATE DATABASE `dbo`;

CREATE TABLE `Student` (
  `Username` varchar(8) CHARACTER SET utf8mb4 NOT NULL,
  `Name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Professor` (
  `Username` varchar(8) CHARACTER SET utf8mb4 NOT NULL,
  `Name` varchar(30) CHARACTER SET utf8mb4 NOT NULL,
  `Rating` double NOT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

 CREATE TABLE `Student` (
  `Username` varchar(8) CHARACTER SET utf8mb4 NOT NULL,
  `Name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Class` (
  `CourseNum` varchar(10) NOT NULL,
  `CourseName` varchar(50) DEFAULT NULL,
  `CreditHours` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`CourseNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Section` (
  `CRN` smallint(6) NOT NULL,
  `CourseNum` varchar(10) DEFAULT NULL,
  `Period` varchar(10) DEFAULT NULL,
  `ProfUsername` varchar(8) CHARACTER SET utf8mb4 DEFAULT NULL,
  `DaysOfWeek` varchar(5) DEFAULT NULL,
  `SectionNum` tinyint(3) DEFAULT NULL,
  PRIMARY KEY (`CRN`),
  KEY `FK_Section_Professor` (`ProfUsername`),
  KEY `FK_Section_Class` (`CourseNum`),
  CONSTRAINT `FK_Section_Class` FOREIGN KEY (`CourseNum`) REFERENCES `Class` (`CourseNum`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Section_Professor` FOREIGN KEY (`ProfUsername`) REFERENCES `Professor` (`Username`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `SectionRoster` (
  `CRN` smallint(6) NOT NULL,
  `StudentUsername` varchar(8) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`CRN`,`StudentUsername`),
  KEY `FK_SectionRoster_Student` (`StudentUsername`),
  CONSTRAINT `FK_SectionRoster_Section` FOREIGN KEY (`CRN`) REFERENCES `Section` (`CRN`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_SectionRoster_Student` FOREIGN KEY (`StudentUsername`) REFERENCES `Student` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `FavoritedSchedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Flag` int(11) NOT NULL,
  `StudentUsername` varchar(8) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Favorited_Schedule_Student` (`StudentUsername`),
  CONSTRAINT `FK_Favorited_Schedule_Student` FOREIGN KEY (`StudentUsername`) REFERENCES `Student` (`Username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;

CREATE TABLE `FavoritedScheduleClassList` (
  `id` int(11) NOT NULL,
  `CRN` smallint(6) NOT NULL,
  PRIMARY KEY (`id`,`CRN`),
  KEY `FK_Favorited_Schedule_Class_List_Section` (`CRN`),
  CONSTRAINT `FK_Favorited_Schedule_Class_List_Favorited_Schedule` FOREIGN KEY (`id`) REFERENCES `FavoritedSchedule` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Favorited_Schedule_Class_List_Section` FOREIGN KEY (`CRN`) REFERENCES `Section` (`CRN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

