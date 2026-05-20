CREATE DATABASE  IF NOT EXISTS `student_performance` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `student_performance`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: student_performance
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `details` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,NULL,'INSERT','Added student: Deepika','2026-05-20 11:56:00'),(2,7,'UPDATE','Updated student: Dipshikha','2026-05-20 12:00:24'),(3,NULL,'INSERT','Added student: Himankana','2026-05-20 12:03:05'),(4,NULL,'INSERT','Added student: Helena','2026-05-20 12:03:45'),(5,NULL,'INSERT','Added student: Yash','2026-05-20 12:04:44'),(6,NULL,'DELETE','Deleted student: Yash','2026-05-20 12:05:12'),(7,NULL,'UPDATE','Updated student: Deepika','2026-05-20 13:24:54'),(8,NULL,'UPDATE','Updated student: Hima','2026-05-20 13:27:47'),(9,NULL,'INSERT','Added student: Debanjana','2026-05-20 14:21:30'),(10,NULL,'UPDATE','Updated student: Himankana','2026-05-20 14:22:51'),(11,NULL,'INSERT','Added student: Vidhi','2026-05-20 17:16:18'),(12,NULL,'UPDATE','Updated student: Vidhi','2026-05-20 17:17:09'),(13,NULL,'UPDATE','Updated student: Vidhi','2026-05-20 17:21:18'),(14,NULL,'INSERT','Added student: Ankitha','2026-05-20 17:42:11'),(15,7,'UPDATE','Updated student: Dipshikha','2026-05-20 17:45:00'),(16,4,'UPDATE','Updated student: Ishita','2026-05-20 19:02:09'),(17,NULL,'INSERT','Added student: Srujana','2026-05-20 19:03:27'),(18,5,'UPDATE','Updated student: Soumavo','2026-05-20 19:04:44'),(19,4,'UPDATE','Updated student: Ishita','2026-05-20 19:05:54'),(20,6,'UPDATE','Updated student: Sanjoli','2026-05-20 19:06:36'),(21,7,'UPDATE','Updated student: Dipshikha','2026-05-20 19:07:32'),(22,8,'UPDATE','Updated student: Raj','2026-05-20 19:08:18'),(23,9,'UPDATE','Updated student: Mrinalini','2026-05-20 19:08:54'),(24,NULL,'UPDATE','Updated student: Deepika','2026-05-20 19:09:33'),(25,NULL,'UPDATE','Updated student: Himankana','2026-05-20 19:10:04'),(26,NULL,'UPDATE','Updated student: Helena','2026-05-20 19:10:46'),(27,NULL,'UPDATE','Updated student: Debanjana','2026-05-20 19:11:27'),(28,NULL,'UPDATE','Updated student: Vidhi','2026-05-20 19:12:38'),(29,NULL,'UPDATE','Updated student: Ankitha','2026-05-20 19:13:13'),(30,10,'UPDATE','Updated student: Deepika','2026-05-20 19:23:55'),(31,11,'UPDATE','Updated student: Himankana','2026-05-20 19:24:34'),(32,12,'UPDATE','Updated student: Helena','2026-05-20 19:25:08'),(33,14,'UPDATE','Updated student: Debanjana','2026-05-20 19:25:44'),(34,15,'UPDATE','Updated student: Vidhi','2026-05-20 19:26:15'),(35,16,'UPDATE','Updated student: Ankitha','2026-05-20 19:26:48'),(36,17,'UPDATE','Updated student: Srujana','2026-05-20 19:27:08'),(37,NULL,'INSERT','Added student: Anushka','2026-05-20 19:41:15'),(38,5,'UPDATE','Updated student: Soumavo','2026-05-20 20:05:01'),(40,18,'UPDATE','Updated student: Anushka','2026-05-20 20:08:50'),(41,5,'UPDATE','Updated student: Soumavo','2026-05-20 20:15:15');
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(50) NOT NULL,
  `details` text NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,1,'INSERT','Added student: Anushka','2026-05-20 19:41:15'),(2,1,'CREDENTIAL_RESET','Administrative forced password override for profile user: admin','2026-05-20 19:54:04'),(3,1,'CREDENTIAL_RESET','Administrative forced password override for profile user: faculty','2026-05-20 19:54:33'),(4,1,'CREDENTIAL_RESET','Administrative forced password override for profile user: admin','2026-05-20 20:05:35'),(5,1,'CREDENTIAL_RESET','Administrative forced password override for profile user: faculty','2026-05-20 20:14:49'),(6,1,'BONUS_GRANT','Awarded +3 extra credits to student: Soumavo (ID: 2)','2026-05-20 20:15:15');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `department` varchar(50) NOT NULL,
  `marks` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `enrolled_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `maths` int DEFAULT '0',
  `science` int DEFAULT '0',
  `english` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `students_chk_1` CHECK (((`marks` >= 0) and (`marks` <= 100)))
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Ishita','Biochemistry',79,4,'2026-05-18 18:08:56',61,78,98),(2,'Soumavo','Biomedical',80,5,'2026-05-18 18:09:33',42,100,100),(6,'Sanjoli','CSE',73,6,'2026-05-18 20:20:20',99,76,45),(7,'Dipshikha','CSE',76,7,'2026-05-18 20:20:51',66,87,76),(8,'Raj','Biotechnology',62,8,'2026-05-18 20:21:17',21,67,99),(9,'Mrinalini','Biochemistry',59,9,'2026-05-18 20:21:47',34,87,56),(10,'Deepika','AIML',66,10,'2026-05-20 11:56:00',87,45,67),(11,'Himankana','Biomedical',84,11,'2026-05-20 12:03:05',67,88,98),(12,'Helena','AIML',62,12,'2026-05-20 12:03:45',78,87,21),(14,'Debanjana','CSE',44,14,'2026-05-20 14:21:30',34,54,45),(15,'Vidhi','AIML',84,15,'2026-05-20 17:16:18',78,98,76),(16,'Ankitha','CSE',84,16,'2026-05-20 17:42:11',77,98,79),(17,'Srujana','CSE',84,17,'2026-05-20 19:03:27',89,78,87),(18,'Anushka','Biomedical',76,18,'2026-05-20 19:41:15',34,99,97);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `student_insert_log` AFTER INSERT ON `students` FOR EACH ROW BEGIN

INSERT INTO audit_log(user_id, action, details)

VALUES(
NEW.user_id,
'INSERT',
CONCAT('Added student: ', NEW.name)
);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `student_update_log` AFTER UPDATE ON `students` FOR EACH ROW BEGIN

INSERT INTO audit_log(user_id, action, details)

VALUES(
NEW.user_id,
'UPDATE',
CONCAT('Updated student: ', NEW.name)
);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `student_delete_log` AFTER DELETE ON `students` FOR EACH ROW BEGIN

INSERT INTO audit_log(user_id, action, details)

VALUES(
OLD.user_id,
'DELETE',
CONCAT('Deleted student: ', OLD.name)
);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `role` enum('admin','faculty','student') NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270','admin',1,'2026-05-18 14:23:43'),(2,'faculty','682cf6edb46da08293dc9d5b68bc9fc879117ef4e2a461e060a100e057af4882','faculty',1,'2026-05-18 14:25:30'),(3,'student','703b0a3d6ad75b649a28adde7d83c6251da457549263bc7ff45ec709b0a8448b','student',1,'2026-05-18 14:25:42'),(4,'ishita','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:19:28'),(5,'soumavo','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:19:37'),(6,'sanjoli','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:19:48'),(7,'deepshikha','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:22:24'),(8,'raj','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:23:52'),(9,'mrinalini','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 11:37:55'),(10,'Main_admin','c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646','admin',1,'2026-05-20 13:06:59'),(11,'Faculty_1','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5','faculty',1,'2026-05-20 13:08:37'),(12,'deepika','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:23:45'),(13,'himankana','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:24:26'),(14,'helena','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:25:03'),(15,'debanjana','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:25:43'),(16,'vidhi','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:26:14'),(17,'ankitha','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:26:46'),(18,'srujana','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 19:27:06'),(20,'anushka','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','student',1,'2026-05-20 20:08:44');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'student_performance'
--

--
-- Dumping routines for database 'student_performance'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-21  2:05:13
