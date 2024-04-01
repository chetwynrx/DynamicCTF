-- Adminer 4.8.1 MySQL 8.0.28 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET GLOBAL foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `example`;
CREATE DATABASE `example` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `example`;

CREATE TABLE `customers` (
  `name` varchar(100) NOT NULL,
  `company` varchar(100) NOT NULL,
  `surname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `customers` (`name`, `company`, `surname`) VALUES
('Robert',	'UiO',	'Chetwyn'),
('Laszlo',	'NTNU',	'Erdodi'),
('Fabio',	'University of Warwick',	'Zennaro'),
('Åvald',	'UiO',	'Sommervoll'),
('{Bool-Flag}',	'dwap00wj130991190jdopapok109u',	'This_Is_Impossible_Apparently')
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`), `company` = VALUES(`company`), `surname` = VALUES(`surname`);

CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `flag` varchar(100) NOT NULL,
  `surname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users` (`username`, `password`, `flag`, `surname`) VALUES
('robert',	'password1',	'',	'Chetwyn'),
('laszlo',	'password2',	'am i the flag?',	'Erdodi'),
('fabio',	'password3',	'',	'Zennaro'),
('avald',	'password4',	'',	'Sommervoll')
ON DUPLICATE KEY UPDATE `username` = VALUES(`username`), `password` = VALUES(`password`), `flag` = VALUES(`flag`), `surname` = VALUES(`surname`);

-- 2022-05-24 12:07:00
