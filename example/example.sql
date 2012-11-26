-- MySQL dump 10.13  Distrib 5.1.61, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: example
-- ------------------------------------------------------
-- Server version	5.1.61-0+squeeze1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `app_person`
--

LOCK TABLES `app_person` WRITE;
/*!40000 ALTER TABLE `app_person` DISABLE KEYS */;
INSERT INTO `app_person` VALUES (1,0,'2000-01-01 00:00:00',NULL,'Василий','Пупкин',6000,1);
/*!40000 ALTER TABLE `app_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_person_temporal`
--

LOCK TABLES `app_person_temporal` WRITE;
/*!40000 ALTER TABLE `app_person_temporal` DISABLE KEYS */;
INSERT INTO `app_person_temporal` VALUES (0,'2000-05-10 00:00:00','2004-12-31 00:00:00','Василий','Пупкин',7000,1,1,'2012-02-21 23:14:15','I',1),(0,'2005-01-01 00:00:00','2007-05-13 00:00:00','Василий','Пупкин',12000,1,2,'2012-02-21 23:16:59','U',1),(0,'2010-01-01 00:00:00','2012-01-31 00:00:00','Василий','Пупкин',17000,1,3,'2012-02-21 23:17:45','U',1),(0,'2012-02-01 00:00:00','2012-05-13 00:00:00','Василий','Пупкин',20000,1,4,'2012-02-21 23:19:02','U',1),(0,'2012-05-14 00:00:00',NULL,'Василий','Пупкин',21000,1,5,'2012-02-26 22:46:54','U',1),(0,'2007-05-14 00:00:00','2009-12-31 00:00:00','Василий','Пупкин',15000,1,6,'2012-02-26 22:50:28','U',1),(0,'2000-01-01 00:00:00','2000-05-09 00:00:00','Василий','Пупкин',6000,1,7,'2012-02-26 22:51:47','U',1);
/*!40000 ALTER TABLE `app_person_temporal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_organization`
--

LOCK TABLES `app_organization` WRITE;
/*!40000 ALTER TABLE `app_organization` DISABLE KEYS */;
INSERT INTO `app_organization` VALUES (1,0,'2012-01-11 00:00:00',NULL,'Муниципальное казенное учреждение \"Тюменьгортранс\"');
/*!40000 ALTER TABLE `app_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_organization_temporal`
--

LOCK TABLES `app_organization_temporal` WRITE;
/*!40000 ALTER TABLE `app_organization_temporal` DISABLE KEYS */;
INSERT INTO `app_organization_temporal` VALUES (0,'1997-01-31 00:00:00','2004-06-30 00:00:00','Муниципальное унитарное предприятие городского транспорта \"Тюменьгортранс\"',1,'2012-02-21 06:06:06','I',1),(0,'2004-07-01 00:00:00','2012-01-10 00:00:00','Муниципальное учреждение пассажирского городского транспорта \"Тюменьгортранс\"',2,'2012-02-21 06:09:50','U',1),(0,'2012-01-11 00:00:00',NULL,'Муниципальное казенное учреждение \"Тюменьгортранс\"',3,'2012-02-21 06:10:48','U',1);
/*!40000 ALTER TABLE `app_organization_temporal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_group`
--

LOCK TABLES `app_group` WRITE;
/*!40000 ALTER TABLE `app_group` DISABLE KEYS */;
INSERT INTO `app_group` VALUES (1,0,'2012-01-01 00:00:00',NULL,'Первая'),(2,0,'2011-01-01 00:00:00',NULL,'1я');
/*!40000 ALTER TABLE `app_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_group_temporal`
--

LOCK TABLES `app_group_temporal` WRITE;
/*!40000 ALTER TABLE `app_group_temporal` DISABLE KEYS */;
INSERT INTO `app_group_temporal` VALUES (0,'2012-01-01 00:00:00',NULL,'Первая',1,'2012-03-11 05:30:47','I',1),(0,'2011-01-01 00:00:00',NULL,'1я',2,'2012-03-11 05:41:46','I',2);
/*!40000 ALTER TABLE `app_group_temporal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_persongroup`
--

LOCK TABLES `app_persongroup` WRITE;
/*!40000 ALTER TABLE `app_persongroup` DISABLE KEYS */;
INSERT INTO `app_persongroup` VALUES (1,0,'2012-01-01 00:00:00',NULL,1,1);
/*!40000 ALTER TABLE `app_persongroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `app_persongroup_temporal`
--

LOCK TABLES `app_persongroup_temporal` WRITE;
/*!40000 ALTER TABLE `app_persongroup_temporal` DISABLE KEYS */;
INSERT INTO `app_persongroup_temporal` VALUES (0,'2012-01-01 00:00:00',NULL,1,1,1,'2012-03-11 05:43:21','I',1);
/*!40000 ALTER TABLE `app_persongroup_temporal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-03-11 16:54:56
