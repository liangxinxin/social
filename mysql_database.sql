-- MySQL dump 10.13  Distrib 5.7.13, for osx10.11 (x86_64)
--
-- Host: localhost    Database: social
-- ------------------------------------------------------
-- Server version	5.7.13

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
-- Table structure for table `community`
--

DROP TABLE IF EXISTS `community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `describe` varchar(500) DEFAULT NULL,
  `head_img_url` varchar(500) DEFAULT NULL,
  `user_num` int(10) DEFAULT NULL,
  `post_num` int(11) DEFAULT NULL,
  `create_user_id` int(11) DEFAULT NULL,
  `last_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `create_user_id` (`create_user_id`),
  CONSTRAINT `community_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `community`
--

LOCK TABLES `community` WRITE;
/*!40000 ALTER TABLE `community` DISABLE KEYS */;
INSERT INTO `community` VALUES (1,'股票',NULL,NULL,NULL,NULL,NULL,'2016-09-22 03:11:11',NULL),(2,'undefined','finance home','http://',1,0,1,'2016-09-27 11:31:00','2016-09-27 19:30:59'),(3,'undefined','finance home','http://',1,0,1,'2016-09-27 11:44:54','2016-09-27 19:44:54'),(4,'undefined','finance home','http://',1,0,1,'2016-09-27 11:46:31','2016-09-27 19:46:31'),(5,'undefined','finance home','http://',1,0,1,'2016-09-27 11:46:52','2016-09-27 19:46:52'),(6,'undefined','finance home','http://',1,0,1,'2016-09-27 11:50:48','2016-09-27 19:50:48'),(7,'undefined','finance home','http://',1,0,1,'2016-09-28 02:32:00','2016-09-28 10:32:00'),(8,'undefined','finance home','http://',1,0,1,'2016-09-28 02:55:56','2016-09-28 10:55:55'),(9,'undefined','finance home','http://',1,0,1,'2016-09-28 02:59:26','2016-09-28 10:59:26'),(10,'undefined','finance home','http://',1,0,1,'2016-09-28 02:59:58','2016-09-28 10:59:58'),(11,'undefined','finance home','http://',1,0,1,'2016-09-28 03:00:26','2016-09-28 11:00:26'),(12,'undefined','finance home','http://',1,0,1,'2016-09-28 03:01:21','2016-09-28 11:01:21'),(13,'undefined','finance home','http://',1,0,1,'2016-09-28 03:01:45','2016-09-28 11:01:45'),(14,'undefined','finance home','http://',1,0,1,'2016-09-28 03:03:51','2016-09-28 11:03:51'),(15,'唐宁岛','finance home','http://',1,0,1,'2016-09-28 03:04:36','2016-09-28 11:04:36'),(16,'雅虎岛','finance home','http://',1,0,1,'2016-09-28 03:12:47','2016-09-28 11:12:47'),(17,'宜人贷岛','finance home','http://',1,0,1,'2016-09-28 03:38:33','2016-09-28 11:38:33'),(18,'冒险岛岛','finance home','http://',1,0,1,'2016-09-28 03:44:02','2016-09-28 11:44:02'),(19,'金融岛','finance home','http://',1,0,1,'2016-09-28 03:48:32','2016-09-28 11:48:31'),(20,'炒股岛','finance home','http://',1,0,1,'2016-09-28 03:50:27','2016-09-28 11:50:27'),(21,'奇怪岛','finance home','http://',1,0,1,'2016-09-28 03:52:30','2016-09-28 11:52:30'),(22,'新奇岛','finance home','http://',1,0,1,'2016-09-28 03:57:28','2016-09-28 11:57:28'),(23,'外汇岛','finance home','http://',1,0,1,'2016-09-28 04:02:01','2016-09-28 12:02:01'),(24,'宜信岛','finance home','http://',1,0,1,'2016-09-28 04:04:45','2016-09-28 12:04:45');
/*!40000 ALTER TABLE `community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(1500) DEFAULT NULL,
  `content` text,
  `create_user_id` int(11) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  `floor_num` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `create_user_id` (`create_user_id`),
  KEY `community_id` (`community_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,'undefined','undefined',1,1,0,'2016-09-23 17:25:39','2016-09-23 17:25:39'),(2,'undefined','undefined',1,1,0,'2016-09-23 17:50:05','2016-09-23 17:50:05'),(3,'undefined','undefined',1,1,0,'2016-09-23 17:52:14','2016-09-23 17:52:14'),(4,'股票','股票',1,1,0,'2016-09-23 17:53:13','2016-09-23 17:53:13'),(5,'我喜欢股票','别整事',1,1,0,'2016-09-23 18:35:14','2016-09-23 18:35:14'),(6,'哈哈哈','哈哈哈',1,1,0,'2016-09-23 18:39:00','2016-09-23 18:39:00'),(7,'哈哈哈','别整事',1,1,0,'2016-09-23 18:40:58','2016-09-23 18:40:58'),(8,'哈哈哈','别整事',1,1,0,'2016-09-23 18:41:42','2016-09-23 18:41:42'),(9,'哈哈哈','别整事',1,1,0,'2016-09-23 18:42:13','2016-09-23 18:42:13'),(10,'哈哈哈','别整事',1,1,0,'2016-09-23 18:57:52','2016-09-23 18:57:52'),(11,'哈哈','这个不错',1,1,0,'2016-09-26 10:46:16','2016-09-26 10:46:16'),(12,'宜信公司哪款产品好？','我觉得宜人贷貌似还可以',1,1,0,'2016-09-26 10:50:57','2016-09-26 10:50:57'),(13,'宜农贷怎么样？','个人感觉好像喔喔，那一天索菲姐姐我耳机哦我就佛山接发到手机发的身份的时间范德萨范德萨',1,1,0,'2016-09-26 10:53:14','2016-09-26 10:53:14'),(14,'评价一下宜人贷的快速批贷','吉林省流量了算了算了算了算了算了算了老师 ；是；是；是；是；是；的；开始了奋斗开始；疯狂的酸辣粉的康师傅；的萨拉开房大厦开房大厦；分肯定是；浪费肯定是；浪费肯定是了；疯狂的身份；的是开发；独守空房啦；是开发大；按时付款的萨拉方式打开；了',1,1,0,'2016-09-26 10:58:35','2016-09-26 10:58:35'),(15,'评价一下宜人贷的快速批贷','吉林省流量了算了算了算了算了算了算了老师 ；是；是；是；是；是；的；开始了奋斗开始；疯狂的酸辣粉的康师傅；的萨拉开房大厦开房大厦；分肯定是；浪费肯定是；浪费肯定是了；疯狂的身份；的是开发；独守空房啦；是开发大；按时付款的萨拉方式打开；了',1,1,0,'2016-09-26 10:59:22','2016-09-26 10:59:22'),(16,'测试一下新的','测试的二级果好还算是不错错吧，我直冲我信访一个附近的咖啡机的咖啡机的萨法时间反馈时间发了啥看法几点睡了附近的历史 积分打开了手机发送的领导是解放军领导说',1,1,0,'2016-09-26 11:01:01','2016-09-26 11:01:01'),(17,'我要是再测试下新的呢','怎么的，我就是想再测试下新的',1,1,0,'2016-09-26 11:54:18','2016-09-26 11:54:18'),(18,'我再在测试下又能如何','嘿嘿我又要测试新的了',1,1,0,'2016-09-26 11:54:40','2016-09-26 11:54:40'),(19,'哈哈','我是第一个！',1,1,0,'2016-09-27 17:32:58','2016-09-27 17:32:58'),(20,'股票','股票',1,1,0,'2016-09-27 19:22:13','2016-09-27 19:22:13'),(21,'外汇','外汇岛',1,23,0,'2016-09-28 12:03:50','2016-09-28 12:03:50'),(22,'宜信','宜信',1,24,0,'2016-09-28 12:04:52','2016-09-28 12:04:52');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `create_user_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `floor` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `create_user_id` (`create_user_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `reply_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `reply_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `age` smallint(4) DEFAULT NULL,
  `sex` tinyint(2) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `professional` varchar(300) DEFAULT NULL,
  `head_img_url` varchar(500) DEFAULT NULL,
  `location` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'me',20,1,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_community`
--

DROP TABLE IF EXISTS `user_community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `community_id` (`community_id`),
  CONSTRAINT `user_community_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_community_ibfk_2` FOREIGN KEY (`community_id`) REFERENCES `community` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_community`
--

LOCK TABLES `user_community` WRITE;
/*!40000 ALTER TABLE `user_community` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_community` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-28 14:45:20
