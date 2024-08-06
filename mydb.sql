-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-07-29 14:16:36
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `mydb`
--

-- --------------------------------------------------------

--
-- 資料表結構 `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `account` varchar(45) NOT NULL,
  `admin_salt` varchar(64) NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `permission` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `admin_credential`
--

CREATE TABLE `admin_credential` (
  `hash_id` int(11) NOT NULL,
  `hash_admin_id` int(11) NOT NULL,
  `hash_admin_pwd` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `character`
--

CREATE TABLE `character` (
  `character_id` int(11) NOT NULL,
  `character` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `character_record`
--

CREATE TABLE `character_record` (
  `record_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `character_id` int(11) NOT NULL,
  `practice_score` int(11) NOT NULL,
  `study_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `course`
--

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL,
  `course_name` varchar(45) NOT NULL,
  `course_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `course_change`
--

CREATE TABLE `course_change` (
  `changelog_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `change_description` text DEFAULT NULL,
  `course_changecol` varchar(45) DEFAULT NULL,
  `change_by` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `course_character_relation`
--

CREATE TABLE `course_character_relation` (
  `course_character_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `character_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `external_account_binding`
--

CREATE TABLE `external_account_binding` (
  `binding_id` int(11) NOT NULL,
  `binding_user_id` int(11) NOT NULL,
  `acc_identifier` varchar(255) DEFAULT NULL,
  `acc_type` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `study_record`
--

CREATE TABLE `study_record` (
  `record_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `study_progress` int(11) NOT NULL,
  `study_score` int(11) NOT NULL,
  `study_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `account` varchar(45) NOT NULL,
  `name` varchar(100) NOT NULL,
  `user_salt` varchar(64) NOT NULL,
  `is_filed` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`user_id`, `account`, `name`, `user_salt`, `is_filed`) VALUES
(0, 'user1', '徐韻蕎\r\n', 'wISwhs2h\r\n', 0),
(1, 'user2', '徐乙庭\r\n', 'MYeDRN2U\r\n', 0),
(2, 'user3', '陳育鐸\r\n\r\n', 'jJr2I18X\r\n', 0),
(3, 'user4', '詩驛莛\r\n\r\n', 'mbdUs1ij\r\n', 0),
(4, 'user5', '莫凱傑\r\n', 'gF2kV8yH\r\n', 0),
(5, 'user6', '孫詠淳\r\n', 'DdgeMD9i\r\n', 0),
(6, 'user7', '鄭宇翔\r\n', 'fF2KmaN6\r\n', 0),
(7, 'user8', '林庠毅\r\n', 'ESEI4lmY\r\n', 0),
(8, 'user9', '曾嬿儒\r\n', 'BlB84olh\r\n', 0);

-- --------------------------------------------------------

--
-- 資料表結構 `user_credential`
--

CREATE TABLE `user_credential` (
  `hash_id` int(11) NOT NULL,
  `hash_user_id` int(11) NOT NULL,
  `hash_user_pwd` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 傾印資料表的資料 `user_credential`
--

INSERT INTO `user_credential` (`hash_id`, `hash_user_id`, `hash_user_pwd`, `created_at`, `update_at`) VALUES
(0, 0, 'f1f6a33b469846f6b6d91df1822d65a5eb6d5f93f6aecad2c76b07dd374cee0f\r\n\r\n', '2024-07-17 18:56:51', NULL),
(1, 1, '38f0b2fdd8aee7531ab418b118423f368ab760429123b99886cc2147aadbb467\r\n', '2024-07-17 18:56:51', NULL),
(2, 2, 'd51027a690a8bc0420a8875afb7bbcf4954cdd7700b3b60fac2c1dc5d52731d9\r\n', '2024-07-17 18:56:51', NULL),
(3, 3, '1f3d3a67fa887e1e39ca95f65cb932400f61407fcc78eebec57280bbc77f195e\r\n', '2024-07-17 18:56:51', NULL),
(4, 4, '628acd7a67ad1a3600ac8dcd133cab39b8a616fe6d467825d65b7addf024ffca\r\n', '2024-07-17 18:56:51', NULL),
(5, 5, 'd7e6d3ae7f39f5089aaf61c7d0ff05e6c625815da88b36e5ba903f6d916fed45\r\n', '2024-07-17 18:56:51', NULL),
(6, 6, '6dbec15151b49781d28083703c6291b83d1dc50497be379fcaf44184c084b554', '2024-07-17 18:56:51', NULL),
(7, 7, '1c7eb08c4282b95d3ca4feb9570905dfd5368242586c58739dbbeacd0affb86c', '2024-07-17 18:56:51', NULL),
(8, 8, '9ad7e01c0554ed2c512ba57c3b35f9595b8baae198f7794f8be199a286b2b974\r\n', '2024-07-17 18:56:51', NULL);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `admin_id_UNIQUE` (`admin_id`),
  ADD UNIQUE KEY `account_UNIQUE` (`account`),
  MODIFY COLUMN `admin_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `admin_credential`
--
ALTER TABLE `admin_credential`
  ADD PRIMARY KEY (`hash_id`),
  ADD UNIQUE KEY `hash_id_UNIQUE` (`hash_id`),
  ADD UNIQUE KEY `hash_admin_id_UNIQUE` (`hash_admin_id`),
  MODIFY COLUMN `hash_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `character`
--
ALTER TABLE `character`
  ADD PRIMARY KEY (`character_id`),
  ADD UNIQUE KEY `character_id_UNIQUE` (`character_id`),
  ADD UNIQUE KEY `character_UNIQUE` (`character`),
  MODIFY COLUMN `character_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `character_record`
--
ALTER TABLE `character_record`
  ADD PRIMARY KEY (`record_id`,`user_id`,`character_id`),
  ADD UNIQUE KEY `record_id_UNIQUE` (`record_id`),
  ADD KEY `user_character_record_idx` (`user_id`),
  ADD KEY `char_char_record_fk_idx` (`character_id`),
  MODIFY COLUMN `record_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`),
  ADD UNIQUE KEY `course_id_UNIQUE` (`course_id`),
  MODIFY COLUMN `course_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `course_change`
--
ALTER TABLE `course_change`
  ADD PRIMARY KEY (`changelog_id`,`course_id`,`change_by`),
  ADD KEY `course_course_change_fk_idx` (`course_id`),
  ADD KEY `admin_course_change_fk_idx` (`change_by`),
  MODIFY COLUMN `changelog_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `course_character_relation`
--
ALTER TABLE `course_character_relation`
  ADD PRIMARY KEY (`course_character_id`),
  ADD UNIQUE KEY `course_character_id_UNIQUE` (`course_character_id`),
  ADD KEY `course_course_char_relation_fk_idx` (`course_id`),
  ADD KEY `char_course_char_relation_fk_idx` (`character_id`),
  MODIFY COLUMN `course_character_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `external_account_binding`
--
ALTER TABLE `external_account_binding`
  ADD PRIMARY KEY (`binding_id`,`binding_user_id`),
  ADD UNIQUE KEY `binding_id_UNIQUE` (`binding_id`),
  ADD KEY `user_acc_binding_fk` (`binding_user_id`),
  MODIFY COLUMN `binding_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `study_record`
--
ALTER TABLE `study_record`
  ADD PRIMARY KEY (`record_id`,`user_id`,`course_id`),
  ADD UNIQUE KEY `record_id_UNIQUE` (`record_id`),
  ADD KEY `user_study_record_fk_idx` (`user_id`),
  ADD KEY `course_study_record_idx` (`course_id`),
  MODIFY COLUMN `record_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  ADD UNIQUE KEY `account_UNIQUE` (`account`),
  MODIFY COLUMN `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 資料表索引 `user_credential`
--
ALTER TABLE `user_credential`
  ADD PRIMARY KEY (`hash_id`),
  ADD UNIQUE KEY `hash_id_UNIQUE` (`hash_id`),
  ADD UNIQUE KEY `hash_user_id_UNIQUE` (`hash_user_id`),
  MODIFY COLUMN `hash_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `character_record`
--
ALTER TABLE `character_record`
  ADD CONSTRAINT `char_char_record_fk` FOREIGN KEY (`character_id`) REFERENCES `character` (`character_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `user_character_record_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `course_change`
--
ALTER TABLE `course_change`
  ADD CONSTRAINT `admin_course_change_fk` FOREIGN KEY (`change_by`) REFERENCES `admin` (`admin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `course_course_change_fk` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `course_character_relation`
--
ALTER TABLE `course_character_relation`
  ADD CONSTRAINT `char_course_char_relation_fk` FOREIGN KEY (`character_id`) REFERENCES `character` (`character_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `course_course_char_relation_fk` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `external_account_binding`
--
ALTER TABLE `external_account_binding`
  ADD CONSTRAINT `user_acc_binding_fk` FOREIGN KEY (`binding_user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- 資料表的限制式 `study_record`
--
ALTER TABLE `study_record`
  ADD CONSTRAINT `course_study_record_fk` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `user_study_record_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
