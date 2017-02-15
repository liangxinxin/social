-- MySQL dump 10.13  Distrib 5.7.12, for osx10.11 (x86_64)
--
-- Host: localhost    Database: social
-- ------------------------------------------------------
-- Server version	5.7.12

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
-- Current Database: `social`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `social` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `social`;

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
  `head_img_url` varchar(500) DEFAULT 'https://img3.doubanio.com/icon/g35417-1.jpg',
  `user_num` int(10) DEFAULT NULL,
  `post_num` int(11) DEFAULT NULL,
  `create_user_id` int(11) DEFAULT NULL,
  `last_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `create_user_id` (`create_user_id`),
  CONSTRAINT `community_ibfk_1` FOREIGN KEY (`create_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `community`
--

LOCK TABLES `community` WRITE;
/*!40000 ALTER TABLE `community` DISABLE KEYS */;
INSERT INTO `community` VALUES (1,'股票',NULL,NULL,NULL,NULL,NULL,'2016-09-22 03:11:11',NULL),(33,'白金','白金爱好者','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,1,'2016-10-11 03:22:06','2016-10-11 11:22:06'),(34,'宜信产品','宜信产品讨论基地','https://img3.doubanio.com/icon/g35417-1.jpg',8,4,1,'2016-10-11 09:12:56','2016-10-11 17:12:56'),(35,'期货','期货爱好者的家园！','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,1,'2016-10-20 07:28:59','2016-10-20 15:28:59'),(36,'期货白银','白银期货高手之家园！','https://img3.doubanio.com/icon/g35417-1.jpg',1,6,1,'2016-10-20 07:42:22','2016-10-20 15:42:22'),(37,'圣斗士','你感受到小宇宙了吗？','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,1,'2016-10-21 03:31:33','2016-10-21 11:31:32'),(38,'西游记','唐僧取经灯布冷步登','https://img3.doubanio.com/icon/g35417-1.jpg',1,2,1,'2016-10-21 03:35:40','2016-10-21 11:35:40'),(39,'宜农贷','宜农贷，农民的好帮手','https://img3.doubanio.com/icon/g35417-1.jpg',1,1,2,'2016-10-24 03:25:45','2016-10-24 11:25:45'),(40,'金银','我爱金银','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,2,'2016-10-24 04:19:55','2016-10-24 12:19:55'),(41,'财富','高净值人群的交流场所','https://img3.doubanio.com/icon/g35417-1.jpg',1,2,2,'2016-10-24 08:18:13','2016-10-24 16:18:13'),(42,'股票炒股','我最喜欢炒股','https://img3.doubanio.com/icon/g35417-1.jpg',1,1,2,'2016-10-24 09:36:11','2016-10-24 17:36:11'),(43,'白石山','风景优美','https://img3.doubanio.com/icon/g35417-1.jpg',2,2,3,'2016-10-28 06:44:02','2016-10-28 14:44:02'),(44,'仙人芋','好吃','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,3,'2016-10-28 06:45:34','2016-10-28 14:45:34'),(45,'峡谷','京东大峡谷','https://img3.doubanio.com/icon/g35417-1.jpg',0,0,3,'2016-10-28 06:47:01','2016-10-28 14:47:00'),(46,'东非','美丽的东非大裂谷','https://img3.doubanio.com/icon/g35417-1.jpg',1,1,3,'2016-10-28 06:48:09','2016-10-28 14:48:09'),(47,'宜人贷','人人有信用，信用有价值','https://img3.doubanio.com/icon/g35417-1.jpg',1,3,2,'2016-10-28 07:39:52','2016-10-28 15:39:52'),(48,'房产投资','房产投资爱好者的家园','https://img3.doubanio.com/icon/g35417-1.jpg',1,1,2,'2016-10-28 09:39:04','2016-10-28 17:39:04'),(49,'移民','移民讨论','https://img3.doubanio.com/icon/g35417-1.jpg',1,1,3,'2016-10-28 09:43:49','2016-10-28 17:43:49'),(50,'母基金','母基金','https://img3.doubanio.com/icon/g35417-1.jpg',1,2,2,'2016-10-28 10:12:45','2016-10-28 18:12:45'),(51,'老虎','老虎爱好者的家园','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,2,'2016-11-10 11:23:40','2016-11-10 19:23:40'),(52,'test','testaasdfksdfjsdkjfdsfjsdakfjsdkfjsdkfjsdkfjdskfjdskfjdskfjdskfjsdkfjsdkfjsdkfjsdkfjsdkfjsdkfjdskfjsdsdkfjdskfjsdkfjdskfjsdkfjdskfjasdkfjsakfjsdf','https://img3.doubanio.com/icon/g35417-1.jpg',1,0,2,'2016-12-08 08:40:27','2016-12-08 16:40:27'),(53,'test','testaasdfksdfjsdkjfdsfjsdakfjsdkfjsdkfjsdkfjdskfjdskfjdskfjdskfjsdkfjsdkfjsdkfjsdkfjsdkfjsdkfjdskfjsdsdkfjdskfjsdkfjdskfjsdkfjdskfjasdkfjsakfjsdf','https://img3.doubanio.com/icon/g35417-1.jpg',1,2,2,'2016-12-08 08:43:24','2016-12-08 16:43:24');
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
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,'undefined','undefined',1,1,0,'2016-09-23 17:25:39','2016-09-23 17:25:39'),(2,'undefined','undefined',1,1,0,'2016-09-23 17:50:05','2016-09-23 17:50:05'),(3,'undefined','undefined',1,1,0,'2016-09-23 17:52:14','2016-09-23 17:52:14'),(4,'股票','股票',1,1,0,'2016-09-23 17:53:13','2016-09-23 17:53:13'),(5,'我喜欢股票','别整事',1,1,0,'2016-09-23 18:35:14','2016-09-23 18:35:14'),(6,'哈哈哈','哈哈哈',1,1,0,'2016-09-23 18:39:00','2016-09-23 18:39:00'),(7,'哈哈哈','别整事',1,1,0,'2016-09-23 18:40:58','2016-09-23 18:40:58'),(8,'哈哈哈','别整事',1,1,0,'2016-09-23 18:41:42','2016-09-23 18:41:42'),(9,'哈哈哈','别整事',1,1,0,'2016-09-23 18:42:13','2016-09-23 18:42:13'),(10,'哈哈哈','别整事',1,1,0,'2016-09-23 18:57:52','2016-09-23 18:57:52'),(11,'哈哈','这个不错',1,1,0,'2016-09-26 10:46:16','2016-09-26 10:46:16'),(12,'宜信公司哪款产品好？','我觉得宜人贷貌似还可以',1,1,0,'2016-09-26 10:50:57','2016-09-26 10:50:57'),(13,'宜农贷怎么样？','个人感觉好像喔喔，那一天索菲姐姐我耳机哦我就佛山接发到手机发的身份的时间范德萨范德萨',1,1,0,'2016-09-26 10:53:14','2016-09-26 10:53:14'),(14,'评价一下宜人贷的快速批贷','吉林省流量了算了算了算了算了算了算了老师 ；是；是；是；是；是；的；开始了奋斗开始；疯狂的酸辣粉的康师傅；的萨拉开房大厦开房大厦；分肯定是；浪费肯定是；浪费肯定是了；疯狂的身份；的是开发；独守空房啦；是开发大；按时付款的萨拉方式打开；了',1,1,0,'2016-09-26 10:58:35','2016-09-26 10:58:35'),(15,'评价一下宜人贷的快速批贷','吉林省流量了算了算了算了算了算了算了老师 ；是；是；是；是；是；的；开始了奋斗开始；疯狂的酸辣粉的康师傅；的萨拉开房大厦开房大厦；分肯定是；浪费肯定是；浪费肯定是了；疯狂的身份；的是开发；独守空房啦；是开发大；按时付款的萨拉方式打开；了',1,1,0,'2016-09-26 10:59:22','2016-09-26 10:59:22'),(16,'测试一下新的','测试的二级果好还算是不错错吧，我直冲我信访一个附近的咖啡机的咖啡机的萨法时间反馈时间发了啥看法几点睡了附近的历史 积分打开了手机发送的领导是解放军领导说',1,1,0,'2016-09-26 11:01:01','2016-09-26 11:01:01'),(17,'我要是再测试下新的呢','怎么的，我就是想再测试下新的',1,1,0,'2016-09-26 11:54:18','2016-09-26 11:54:18'),(18,'我再在测试下又能如何','嘿嘿我又要测试新的了',1,1,0,'2016-09-26 11:54:40','2016-09-26 11:54:40'),(19,'哈哈','我是第一个！',1,1,0,'2016-09-27 17:32:58','2016-09-27 17:32:58'),(20,'股票','股票',1,1,6,'2016-09-27 19:22:13','2016-09-27 19:22:13'),(32,'你好','哈哈，这是我的第一个帖子',1,34,0,'2016-10-17 17:13:17','2016-10-17 17:13:17'),(33,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:18:40','2016-10-18 10:18:40'),(34,'请问最好的理财产品是什么','是宜人贷吗？',1,34,0,'2016-10-18 10:22:21','2016-10-18 10:22:21'),(35,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:24:55','2016-10-18 10:24:55'),(36,'我有10万元，怎么投资？','如题',1,34,0,'2016-10-18 10:25:48','2016-10-18 10:25:48'),(37,'我有10万元，怎么投资？','如题',1,34,0,'2016-10-18 10:25:57','2016-10-18 10:25:57'),(38,'我有10万元，怎么投资？','如题',1,34,7,'2016-10-18 10:26:44','2016-10-18 10:26:44'),(39,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:36:15','2016-10-18 10:36:15'),(40,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:36:16','2016-10-18 10:36:16'),(41,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:36:16','2016-10-18 10:36:16'),(42,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:38:25','2016-10-18 10:38:25'),(43,'宜信吧','第二个帖子哦',1,34,1,'2016-10-18 10:38:26','2016-10-18 10:38:26'),(44,'宜信吧','第二个帖子哦',1,34,3,'2016-10-18 10:38:27','2016-10-18 10:38:27'),(45,'宜信吧','第二个帖子哦',1,34,0,'2016-10-18 10:38:27','2016-10-18 10:38:27'),(50,'期货技巧','首先，必须了解什么是期货',1,35,1,'2016-10-20 15:29:33','2016-10-20 15:29:33'),(51,'怎么炒白银能赚大钱？','呵呵，太简单了！我就是靠炒白银起家的！',1,36,0,'2016-10-20 15:42:56','2016-10-20 15:42:56'),(52,'我和白银不得不说的故事','2011年，我买了一公斤白银',1,36,0,'2016-10-20 16:46:28','2016-10-20 16:46:28'),(53,'黄金还是白银？','这是一个问题',1,36,3,'2016-10-20 16:49:15','2016-10-20 16:49:15'),(54,'黄金还是白银？','这是一个问题',1,36,0,'2016-10-20 16:51:57','2016-10-20 16:51:57'),(55,'白银帝国','真的吗？',1,36,2,'2016-10-20 16:52:24','2016-10-20 16:52:24'),(56,'大家快来炒白银呀','哈哈必须炒白银',1,36,0,'2016-10-20 18:02:03','2016-10-20 18:02:03'),(57,'大家快来炒白银呀','哈哈必须炒白银',1,36,0,'2016-10-20 18:02:36','2016-10-20 18:02:36'),(58,'再来一个','第三个',1,36,0,'2016-10-20 18:05:05','2016-10-20 18:05:05'),(59,'再来一个','第三个',1,36,0,'2016-10-20 18:21:09','2016-10-20 18:21:09'),(60,'再来一个','第三个',1,36,0,'2016-10-20 18:21:58','2016-10-20 18:21:58'),(61,'再来一个','第三个',1,36,0,'2016-10-20 18:23:25','2016-10-20 18:23:25'),(62,'第一个，报道！','第一个报道！',1,38,1,'2016-10-21 11:36:05','2016-10-21 11:36:05'),(63,'第二个','嘎啊',1,38,0,'2016-10-21 12:03:02','2016-10-21 12:03:02'),(64,'你好','我是农民',2,39,1,'2016-10-24 11:38:25','2016-10-24 11:38:25'),(65,'你好','这是我的第一个',2,40,0,'2016-10-24 12:20:10','2016-10-24 12:20:10'),(66,'我来了，宜信','超级无敌小飞侠',2,34,0,'2016-10-24 13:54:00','2016-10-24 13:54:00'),(67,'我来了，宜信','超级无敌小飞侠',2,34,23,'2016-10-24 13:57:08','2016-10-24 13:57:08'),(68,'我有10万元，想选择一个投资产品','该选哪个？',2,34,3,'2016-10-24 16:17:32','2016-10-24 16:17:32'),(69,'如何组合投资方式最合理？','请大牛回答',2,41,0,'2016-10-24 16:23:38','2016-10-24 16:23:38'),(70,'3+1组合是最好的方式','海外投资，资产配置',2,41,2,'2016-10-24 16:24:11','2016-10-24 16:24:11'),(71,'炒股赚大钱','一年炒股赚千万！',2,42,5,'2016-10-24 17:36:30','2016-10-24 17:36:30'),(72,'宜农贷怎么样？','感觉还不错',3,34,8,'2016-10-27 11:52:44','2016-10-27 11:52:44'),(73,'你去过吗？','白石山',3,43,0,'2016-10-28 14:44:16','2016-10-28 14:44:16'),(74,'必须去过','我去过',3,43,1,'2016-10-28 14:44:38','2016-10-28 14:44:38'),(75,'哈哈','我来了',3,46,0,'2016-10-28 14:48:29','2016-10-28 14:48:29'),(76,'我有10万元，如何理财比较合适','如题，请高手进来回答',2,47,0,'2016-10-28 15:40:29','2016-10-28 15:40:29'),(77,'宜人贷到底怎么样','听说刚在美国上市了，贷款利率多少？',3,47,0,'2016-10-28 15:41:23','2016-10-28 15:41:23'),(78,'现货金银能赚钱吗？','我前年买的白银，9块钱一克拉买的',2,47,0,'2016-10-28 15:42:28','2016-10-28 15:42:28'),(79,'我有100万，买哪里的房比较好','如题',2,48,1,'2016-10-28 17:39:36','2016-10-28 17:39:36'),(80,'移民都有哪些类别','我想问一下',3,49,5,'2016-10-28 17:44:13','2016-10-28 17:44:13'),(81,'母基金','母基金',2,50,0,'2016-10-28 18:13:16','2016-10-28 18:13:16'),(82,'test post','sdjfdskfjsdkfjdskfjsd\r\ndskfjdsak;fjdsa;fs\r\ndksfjdsa\'fdsa\r\nf',2,50,0,'2016-12-08 11:26:20','2016-12-08 11:26:20'),(83,'test','123456',2,53,0,'2016-12-08 16:59:51','2016-12-08 16:59:51'),(84,'test02','sdfsdfsd',2,53,4,'2016-12-08 17:01:43','2016-12-08 17:01:43');
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
) ENGINE=InnoDB AUTO_INCREMENT=174 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (1,'我买的中兴的股票',1,20,2,'2016-09-29 07:59:06'),(2,'我买的中兴的股票',1,20,3,'2016-09-29 08:01:32'),(3,'我买的中兴的股票',1,20,4,'2016-09-29 08:02:52'),(4,'今年赚了',1,20,5,'2016-09-29 08:03:08'),(5,'真的赚了？',1,20,6,'2016-09-29 08:09:55'),(16,'找宜人贷呀',1,38,1,'2016-10-18 03:26:00'),(17,'找宜人贷呀',1,38,2,'2016-10-18 06:10:41'),(18,'找宜人贷呀',1,38,3,'2016-10-18 06:12:03'),(38,'好办，交给我就行',1,38,4,'2016-10-18 09:53:01'),(39,'哈哈',1,38,5,'2016-10-18 09:53:14'),(40,'确实不错',1,38,6,'2016-10-18 09:54:25'),(57,'确实',1,44,1,'2016-10-18 11:44:10'),(58,'确实',1,44,2,'2016-10-19 03:26:42'),(59,'哈哈',1,38,7,'2016-10-19 07:24:44'),(103,'不错！',1,43,1,'2016-10-19 12:18:26'),(114,'其次，必须了解什么不是期货',1,50,1,'2016-10-20 07:29:50'),(115,'我怎么就觉得不是一个问题呢',1,53,1,'2016-10-20 09:32:47'),(116,'我怎么就觉得不是一个问题呢',1,53,2,'2016-10-20 09:33:24'),(117,'确实是一个问题啊',1,53,3,'2016-10-20 09:41:08'),(118,'真的假的？',1,55,1,'2016-10-20 09:45:26'),(119,'我觉得应该是真的',1,55,2,'2016-10-20 09:45:39'),(120,'确实',1,44,3,'2016-10-20 10:23:04'),(121,'鸟',1,62,1,'2016-10-21 04:03:12'),(122,'我是工人',2,64,1,'2016-10-24 03:44:39'),(123,'这个动画我看过，哈哈',2,67,1,'2016-10-24 06:54:56'),(124,'这个动画我看过，哈哈',2,67,3,'2016-10-24 08:11:39'),(125,'选宜信呀',2,68,1,'2016-10-25 06:19:12'),(126,'都看过',2,67,4,'2016-10-25 06:20:47'),(127,'我是大牛我怕谁？',2,70,1,'2016-10-25 07:06:05'),(128,'我是大牛我怕谁？',2,70,2,'2016-10-25 07:06:14'),(129,'我也看过',2,67,5,'2016-10-25 07:18:30'),(130,'我也看过',2,67,6,'2016-10-25 07:20:55'),(131,'我也看过',2,67,7,'2016-10-25 07:20:56'),(132,'我也看过',2,67,8,'2016-10-25 07:20:56'),(133,'我也看过',2,67,9,'2016-10-25 07:25:50'),(134,'我也看过',2,67,10,'2016-10-25 07:25:52'),(135,'我也看过',2,67,11,'2016-10-25 07:25:53'),(136,'我也看过',2,67,12,'2016-10-25 07:25:53'),(137,'我也看过',2,67,13,'2016-10-25 07:25:53'),(138,'宜信好吗？',2,68,2,'2016-10-25 07:50:45'),(139,'必须好呀',2,68,3,'2016-10-25 07:50:54'),(140,'唬谁呢',2,71,1,'2016-10-25 08:42:35'),(141,'唬谁呢',2,71,2,'2016-10-25 08:45:33'),(142,'唬谁呢',2,71,3,'2016-10-25 08:45:35'),(143,'唬谁呢',2,71,4,'2016-10-25 08:47:50'),(144,'唬谁呢',2,71,5,'2016-10-25 08:47:52'),(145,'确实不错啊，个人觉得',2,72,1,'2016-10-27 03:53:27'),(146,'真的不错哦',2,72,2,'2016-10-28 04:20:48'),(147,'确实不错哦',3,72,3,'2016-10-28 06:19:55'),(148,'真的？',3,72,4,'2016-10-28 06:20:24'),(149,'我有点不信那',3,72,5,'2016-10-28 06:20:41'),(150,'好吧',3,72,6,'2016-10-28 06:21:20'),(151,' 今天天气不错',2,72,7,'2016-10-28 09:37:49'),(152,'我觉得买昌平回龙观的就行',3,79,1,'2016-10-28 09:40:20'),(153,'确实不错啊',3,72,8,'2016-11-03 09:52:00'),(154,'看过+1',3,67,14,'2016-11-17 08:50:38'),(155,'看过+1',3,67,15,'2016-11-17 08:50:47'),(156,'看过加1',3,67,16,'2016-11-17 08:50:58'),(157,'你好',3,67,17,'2016-11-24 06:29:55'),(158,'好',3,67,18,'2016-11-24 06:30:00'),(159,'好',3,67,19,'2016-11-24 06:30:05'),(160,'你好',3,67,20,'2016-11-24 06:30:12'),(161,'你好',3,67,21,'2016-11-24 06:30:19'),(162,'加油，朋友',2,67,22,'2016-11-30 10:10:06'),(163,'加油，朋友',2,67,23,'2016-11-30 10:10:24'),(164,'test111111111111',2,80,1,'2016-12-08 03:17:23'),(165,'test111111111111',2,80,2,'2016-12-08 03:19:25'),(166,'test111111111111',2,80,3,'2016-12-08 03:19:45'),(167,'test111111111111',2,80,4,'2016-12-08 03:19:56'),(168,'test111111111111',2,80,5,'2016-12-08 03:20:13'),(169,'sfjsdkfjsd',2,84,1,'2016-12-08 09:01:49'),(170,'sfsdfjdskf',2,74,1,'2016-12-08 10:16:28'),(171,'sfjsdkfjsd',2,84,2,'2016-12-09 02:19:28'),(172,'sfjsdkfjsd',2,84,3,'2016-12-09 02:20:09'),(173,'sfjsdkfjsd',2,84,4,'2016-12-09 02:20:22');
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply_like_activity`
--

DROP TABLE IF EXISTS `reply_like_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reply_like_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reply_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply_like_activity`
--

LOCK TABLES `reply_like_activity` WRITE;
/*!40000 ALTER TABLE `reply_like_activity` DISABLE KEYS */;
INSERT INTO `reply_like_activity` VALUES (7,173,2,'2016-12-09 18:35:19'),(8,171,2,'2016-12-09 18:35:27'),(9,169,2,'2016-12-09 18:35:41');
/*!40000 ALTER TABLE `reply_like_activity` ENABLE KEYS */;
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
  `password` varchar(150) DEFAULT NULL,
  `age` smallint(4) DEFAULT NULL,
  `sex` tinyint(2) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `professional` varchar(300) DEFAULT NULL,
  `head_img_url` varchar(500) DEFAULT NULL,
  `location` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'股票爱好者','123456',20,1,NULL,NULL,'股票预测师','https://img3.doubanio.com/icon/u3467600-13.jpg',NULL),(2,'盛佳','123456',10,1,'18700139017',NULL,'网信-首席执行官','https://img3.doubanio.com/icon/g10479-3.jpg',NULL),(3,'付红雷','123456',0,2,'1','','宜信-理财规划师','https://img1.doubanio.com/icon/g26926-9.jpg',''),(4,'红雷付','1',0,2,'1','','','',''),(5,'红雷付','1',0,2,'1','','','',''),(6,'红雷付','1',0,2,'1','','','',''),(7,'红雷付','1',0,2,'1','','','',''),(8,'红雷付','1',0,2,'1','','','',''),(9,'红雷付','1',0,2,'1','','','',''),(10,'唐宁','111',0,2,'1','','','',''),(11,'宜人贷','1',0,2,'1','','','',''),(12,'宜农贷','1',0,2,'2','','','',''),(13,'宜商贷','1',0,2,'11','','','',''),(14,'宜商贷','1',0,2,'11','','','',''),(15,'宜商贷','1',0,2,'11','','','',''),(16,'宜商贷','1',0,2,'11','','','',''),(17,'aaaa','111111',0,2,'sdfjdsk','','','https://img3.doubanio.com/icon/g232413-3.jpg','');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_community`
--

LOCK TABLES `user_community` WRITE;
/*!40000 ALTER TABLE `user_community` DISABLE KEYS */;
INSERT INTO `user_community` VALUES (2,3,34,'2016-10-27 09:56:20'),(3,3,34,'2016-10-27 09:57:25'),(4,3,34,'2016-10-27 09:58:27'),(5,3,34,'2016-10-27 09:58:34'),(6,3,34,'2016-10-27 10:15:57'),(12,3,34,'2016-10-28 06:30:29'),(13,3,43,'2016-10-28 06:44:24'),(14,3,45,'2016-10-28 06:47:14'),(15,3,46,'2016-10-28 06:48:16'),(16,2,34,'2016-10-28 07:39:12');
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

-- Dump completed on 2016-12-12 16:08:29

-- add by lxx  添加 default_image 默认数据
DROP TABLE IF EXISTS `default_image`;

CREATE TABLE `default_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(2) DEFAULT NULL,
  `imgsrc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `default_image` WRITE;
/*!40000 ALTER TABLE `default_image` DISABLE KEYS */;

INSERT INTO `default_image` (`id`, `type`, `imgsrc`)
VALUES
	(1,'0','http://0.0.0.0:6100/images/user/default/1.jpg'),
	(2,'0','http://0.0.0.0:6100/images/user/default/2.jpg'),
	(3,'0','http://0.0.0.0:6100/images/user/default/3.jpg'),
	(4,'1','http://0.0.0.0:6100/images/community/default/c1.jpg'),
	(5,'1','http://0.0.0.0:6100/images/community/default/c2.jpg'),
	(6,'1','http://0.0.0.0:6100/images/community/default/c4.jpg'),
	(7,'0','http://0.0.0.0:6100/images/user/default/4.jpg'),
	(8,'1','http://0.0.0.0:6100/images/community/default/c5.jpg'),
	(9,'1','http://0.0.0.0:6100/images/community/default/c6.jpg'),
	(10,'1','http://0.0.0.0:6100/images/community/default/c7.jpg'),
	(11,'1','http://0.0.0.0:6100/images/community/default/c8.jpg'),
	(12,'0','http://0.0.0.0:6100/images/user/default/5.jpg'),
	(13,'0','http://0.0.0.0:6100/images/user/default/6.jpg');

/*!40000 ALTER TABLE `default_image` ENABLE KEYS */;
UNLOCK TABLES;