-- MySQL dump 10.13  Distrib 5.7.14, for Win64 (x86_64)
--
-- Host: localhost    Database: lab5
-- ------------------------------------------------------
-- Server version	5.7.14

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

DROP DATABASE IF EXISTS `lab5`;
CREATE DATABASE `lab5`;
USE `lab5`;
--
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `car` (
  `registration` varchar(15) NOT NULL,
  `make` varchar(20) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `colour` varchar(10) DEFAULT NULL,
  `mileage` integer DEFAULT NULL,
  `engineSize` float(2,1) DEFAULT NULL,
  PRIMARY KEY (`registration`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES ('05-MO-17931','Toyota','Highlander','Green',253789,1.6),('10-G-2334','Toyota','Corolla','Green',123389,1.3),('10-WH-17931','Toyota','Corolla','Silver',130389,1.4),('11-MO-23431','Toyota','Corolla','Black',1234123,1.3),('12-WH-123','Ford','Ka','Black',125882,1.0),('132-G-9923','Ford','Ka','Silver',325883,1.0),('132-MO-19323','Ford','Galaxy','Silver',2343,1.5),('171-G-39532','Toyota','Corolla','Silver',55882,1.3),('171-MO-12533','Ford','Fiesta','Black',25882,1.0),('99-G-300','Toyota','Corolla','Green',599339,1.3);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `personID` integer NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `age` integer DEFAULT NULL,
  `sex` enum('M','F') DEFAULT 'M',
  `isStudent` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`personID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` (`name`,`age`,`sex`,`isStudent`)VALUES ('John',23,'M',1),('Mary',30,'F',0),('Tom',NULL,'M',0),('Alan',18,'M',1),('Laura',17,'F',1),('Bob',18,'M',0);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;
-- Dump completed on 2019-01-14 12:33:21
