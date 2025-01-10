-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: yadra
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('49354ce26234');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branch` (
  `id` varchar(130) NOT NULL,
  `company_id` varchar(130) DEFAULT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(120) NOT NULL,
  `address` varchar(120) NOT NULL,
  `visits` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `branch_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES ('829ccca7-4123-4f13-a785-a410aa2f3ae3','4144bb73-3945-4d6d-82d2-36f6494c94b0','TechCorp Main','main@techcorp.com','1234567890','123 Tech Street',0),('ace1af42-bca2-411d-91d9-bde375544c87','5313149f-6bbf-4d8e-ad17-7e0c54df2963','HealthPlus Central','central@healthplus.com','0987654321','456 Health Avenue',0);
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (4,'Education'),(2,'Healthcare'),(3,'Retail'),(1,'Technology');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `id` varchar(130) NOT NULL,
  `name` varchar(32) NOT NULL,
  `email` varchar(132) NOT NULL,
  `phone` varchar(132) DEFAULT NULL,
  `description` varchar(132) NOT NULL,
  `website` varchar(132) NOT NULL,
  `business_registration` varchar(132) NOT NULL,
  `social_links` varchar(132) NOT NULL,
  `logo` varchar(120) NOT NULL,
  `category` int DEFAULT NULL,
  `address` varchar(120) NOT NULL,
  `created_at` varchar(120) NOT NULL,
  `visits` int DEFAULT NULL,
  `verified` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `business_registration` (`business_registration`),
  UNIQUE KEY `description` (`description`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `social_links` (`social_links`),
  UNIQUE KEY `website` (`website`),
  UNIQUE KEY `phone` (`phone`),
  KEY `category` (`category`),
  CONSTRAINT `company_ibfk_1` FOREIGN KEY (`category`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES ('4144bb73-3945-4d6d-82d2-36f6494c94b0','TechCorp','info@techcorp.com','1234567890','Leading technology solutions provider.','https://techcorp.com','TC12345','https://linkedin.com/company/techcorp','techcorp_logo.png',1,'123 Tech Street','2024-12-12',0,0),('5313149f-6bbf-4d8e-ad17-7e0c54df2963','HealthPlus','contact@healthplus.com','0987654321','Innovative healthcare services.','https://healthplus.com','HP98765','https://facebook.com/healthplus','healthplus_logo.png',2,'456 Health Avenue','2024-12-12',0,0);
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_register`
--

DROP TABLE IF EXISTS `company_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_register` (
  `id` varchar(130) NOT NULL,
  `name` varchar(32) NOT NULL,
  `email` varchar(132) NOT NULL,
  `admin_email` varchar(132) NOT NULL,
  `phone` varchar(132) DEFAULT NULL,
  `description` varchar(132) NOT NULL,
  `website` varchar(132) NOT NULL,
  `business_registration` varchar(132) NOT NULL,
  `social_links` varchar(132) NOT NULL,
  `logo` varchar(120) NOT NULL,
  `category` int DEFAULT NULL,
  `address` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_email` (`admin_email`),
  UNIQUE KEY `business_registration` (`business_registration`),
  UNIQUE KEY `description` (`description`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `social_links` (`social_links`),
  UNIQUE KEY `website` (`website`),
  UNIQUE KEY `phone` (`phone`),
  KEY `category` (`category`),
  CONSTRAINT `company_register_ibfk_1` FOREIGN KEY (`category`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_register`
--

LOCK TABLES `company_register` WRITE;
/*!40000 ALTER TABLE `company_register` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_register` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flagged`
--

DROP TABLE IF EXISTS `flagged`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flagged` (
  `id` varchar(130) NOT NULL,
  `review_id` varchar(130) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `user_id` varchar(130) DEFAULT NULL,
  `flagged_at` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `review_id` (`review_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `flagged_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `review` (`id`) ON DELETE CASCADE,
  CONSTRAINT `flagged_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flagged`
--

LOCK TABLES `flagged` WRITE;
/*!40000 ALTER TABLE `flagged` DISABLE KEYS */;
/*!40000 ALTER TABLE `flagged` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` varchar(130) NOT NULL,
  `review_id` varchar(130) DEFAULT NULL,
  `user_id` varchar(130) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `review_id` (`review_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `review` (`id`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `response` (
  `id` varchar(130) NOT NULL,
  `review_id` varchar(130) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `user_id` varchar(130) DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT NULL,
  `created_at` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `review_id` (`review_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `response_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `review` (`id`),
  CONSTRAINT `response_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
INSERT INTO `response` VALUES ('e73aab51-22ff-441a-9678-12646b24f9bd','31cb7190-811d-4747-8acf-44698b24a2b4','abcd','0ac489dd-9b60-4141-b41a-a2d700d628a1',1,'');
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `id` varchar(130) NOT NULL,
  `user_id` varchar(130) DEFAULT NULL,
  `branch_id` varchar(130) DEFAULT NULL,
  `title` varchar(120) DEFAULT NULL,
  `description` varchar(120) DEFAULT NULL,
  `rating` float NOT NULL,
  `staff_satisfaction` float NOT NULL,
  `speed_satisfaction` float NOT NULL,
  `reliability` float NOT NULL,
  `created_at` varchar(120) NOT NULL,
  `tags` varchar(120) NOT NULL,
  `is_anonymous` tinyint(1) DEFAULT NULL,
  `is_hidden` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `branch_id` (`branch_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`id`) ON DELETE CASCADE,
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES ('31cb7190-811d-4747-8acf-44698b24a2b4','ac2cadd7-9f04-4f29-9830-93868de60a22','829ccca7-4123-4f13-a785-a410aa2f3ae3','Great Experience!','The service was excellent, and the staff was friendly. Highly recommend!',4,4,4,4,'2024-12-12 19:22:29.392605','service,friendly staff',0,1),('3770be31-e139-41f9-b0c1-1220179489df','ac2cadd7-9f04-4f29-9830-93868de60a22','829ccca7-4123-4f13-a785-a410aa2f3ae3','Great Experience!','The service was excellent, and the staff was friendly. Highly recommend!',4,4,4,4,'2024-12-12 19:22:55.150551','service,friendly staff',0,0),('544bc0b8-a90c-48ad-99ae-91deb553489e','ac2cadd7-9f04-4f29-9830-93868de60a22','829ccca7-4123-4f13-a785-a410aa2f3ae3','Great Experience!','The service was excellent, and the staff was friendly. Highly recommend!',4,4,4,4,'2024-12-12 19:22:50.206674','service,friendly staff',0,1);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(4,'branch_admin'),(3,'company_admin'),(2,'user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(130) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(120) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` int DEFAULT NULL,
  `company_id` varchar(130) DEFAULT NULL,
  `branch_id` varchar(130) DEFAULT NULL,
  `created_at` varchar(120) NOT NULL,
  `avatar` varchar(120) NOT NULL,
  `state` int NOT NULL,
  `last_login` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `branch_id` (`branch_id`),
  KEY `company_id` (`company_id`),
  KEY `role` (`role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`id`) ON DELETE CASCADE,
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE,
  CONSTRAINT `users_ibfk_3` FOREIGN KEY (`role`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('0ac489dd-9b60-4141-b41a-a2d700d628a1','email6','$2b$12$/F6YVjdBkzOYQ4jL9IM5mOAD/1qHAlTxyP8Rm1pK2S6.dwX.BXQeO','name6',NULL,3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'2024-12-12 16:04:07.372683','avatar',1,''),('172ad5da-3037-4b3d-8721-3f210d4733da','email5','$2b$12$F.oZcD.MpEk.8Z0AxxSbkePH9CmyGveR2gsH/QblAlKDBuAgRNje6','name5',NULL,3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'2024-12-12 16:03:48.798409','avatar',1,''),('20d60a8e-cb82-46ce-81ff-e6931b0fd644','user@healthplus.com','securepassword','Health User','0987654321',2,'5313149f-6bbf-4d8e-ad17-7e0c54df2963','ace1af42-bca2-411d-91d9-bde375544c87','2024-12-12','user_avatar.png',1,''),('2cdb2f1c-a942-4d1a-a409-c87c20ebc346','email9','$2b$12$Sxpx2yAhZIXV2RKnIzQbZetGyonW1LUgOPbkQVJrkrfazQxKUzHVu','name9',NULL,4,'4144bb73-3945-4d6d-82d2-36f6494c94b0','829ccca7-4123-4f13-a785-a410aa2f3ae3','2024-12-12 16:25:07.257859','avatar',1,''),('6d03bf71-e8df-402b-9996-517561d27294','email@hjkkjhzf.com','$2b$12$gWjsn.g6c9p7cmuCSru3f.BqrH4QuRWKa1O.ML0o1cj7OWb7F7pb2','name10','0555376693',2,NULL,NULL,'<built-in method now of type object at 0x00007FFDF02DAFD0>','avatar',0,''),('7c47b414-de6b-475a-97e0-f0b51cfd5825','email3','$2b$12$c48MdDbrIgHdVAdBo3kbP.QuICh0a6M50ppd2c8JJaoP8MzfcNv5i','name3',NULL,3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'<built-in method now of type object at 0x00007FFEECF0AFD0>','avatar',1,''),('9969d412-2810-4946-9a43-c4f5b81b9123','email8','$2b$12$ARZ3O/rPKGVkxonSEvUpcOGmpNIenuPD3JFLBQhCE0UwKyWA0.beq','name8',NULL,3,NULL,'829ccca7-4123-4f13-a785-a410aa2f3ae3','<built-in method now of type object at 0x00007FFEECF0AFD0>','avatar',1,''),('9c778edf-bc1b-43eb-84bf-c3ed52942252','email2','$2b$12$rhHZAY18YDi4XvnCEDJXMOQoArYRqijYI8DFLaxX9fTmRXmHqn3tS','name2',NULL,3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'<built-in method now of type object at 0x00007FFEECF0AFD0>','avatar',1,''),('ac2cadd7-9f04-4f29-9830-93868de60a22','admin@techcorp.com','securepassword','Tech Admin','1234567890',1,'4144bb73-3945-4d6d-82d2-36f6494c94b0','829ccca7-4123-4f13-a785-a410aa2f3ae3','2024-12-12','admin_avatar.png',1,''),('bcab03bd-8169-4afd-b355-8d93ab3b3b8a','email7','$2b$12$cEnxF.77GfKetqIyoB1md.Zydp88AHEldBPy5GQFswf0XYE3Ygl3G','name7',NULL,3,'5313149f-6bbf-4d8e-ad17-7e0c54df2963',NULL,'2024-12-12 16:13:28.814825','avatar',1,''),('eb4e4372-bd76-4890-883b-d1a434445fac','email','$2b$12$TJ4wxiZcZcpwSxgDZDE0Me.WW65OOv/sJ8CbOPIZrpnTUuH0jcRAy','name',NULL,3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'<built-in method now of type object at 0x00007FFEECF0AFD0>','avatar',1,''),('f5c48730-b8a0-4501-8692-f1584cdc7d58','jane.doe@example.com','$2b$12$uDca/t6Q4N/JW8UmVS0emO4EQxzONNJqUM6KCto9lDhmsmM0hu05q','Jane Doe','+9876543210',3,'4144bb73-3945-4d6d-82d2-36f6494c94b0',NULL,'<built-in method now of type object at 0x00007FFEECF0AFD0>','new_avatar_url_example',1,'');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14  0:56:31
