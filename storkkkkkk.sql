/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - stroke
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`stroke` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `stroke`;

/*Table structure for table `bookings` */

DROP TABLE IF EXISTS `bookings`;

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `consulting_id` int(11) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  `book_date` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

/*Data for the table `bookings` */

insert  into `bookings`(`booking_id`,`user_id`,`consulting_id`,`date_time`,`book_date`,`status`,`time`) values 
(3,1,1,'2025-02-23 12:27:49','2025-02-23','Paid','11:10 - 11:25'),

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `sender_type` varchar(10) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `receiver_type` varchar(10) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`sender_id`,`sender_type`,`receiver_id`,`receiver_type`,`message`,`date_time`) values 
(1,4,'user',2,'doctor','hello','2025-02-23 12:18:02'),


/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaint_id`,`user_id`,`complaint`,`reply`,`date_time`) values 
(1,1,'jdjdjdjd','ok','2025-02-23 12:16:44'),
(2,2,'sdfgvhbjnkm','pending','2025-03-24');

/*Table structure for table `consulting_times` */

DROP TABLE IF EXISTS `consulting_times`;

CREATE TABLE `consulting_times` (
  `consulting_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) DEFAULT NULL,
  `day` varchar(10) DEFAULT NULL,
  `start_time` varchar(10) DEFAULT NULL,
  `end_time` varchar(10) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`consulting_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `consulting_times` */

insert  into `consulting_times`(`consulting_id`,`doctor_id`,`day`,`start_time`,`end_time`,`date_time`) values 
(1,1,'monday','09:00','10:00','2025-02-23 11:09:11'),
(2,2,'monday','09:00','10:00','2025-02-23 11:09:11'),
(3,1,'monday','02:15','03:09','2025-03-24 13:15:43'),
(4,6,'monday','22:34','23:35','2025-03-24 22:34:50');

/*Table structure for table `doctors` */

DROP TABLE IF EXISTS `doctors`;

CREATE TABLE `doctors` (
  `doctor_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `house_name` varchar(20) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `landmark` varchar(50) DEFAULT NULL,
  `qualification` varchar(20) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `path` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`doctor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `doctors` */

insert  into `doctors`(`doctor_id`,`login_id`,`first_name`,`last_name`,`house_name`,`place`,`landmark`,`qualification`,`phone`,`email`,`status`,`path`) values 
(1,2,'alex','g','alex house','ernakulam','MLA Road','MBBS','9876543456','alex@gmail.com','Accepted',NULL),

/*Table structure for table `fee` */

DROP TABLE IF EXISTS `fee`;

CREATE TABLE `fee` (
  `fee_id` int(11) NOT NULL AUTO_INCREMENT,
  `consulting_id` int(11) DEFAULT NULL,
  `amount` varchar(10) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`fee_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `fee` */

insert  into `fee`(`fee_id`,`consulting_id`,`amount`,`date_time`) values 
(1,1,'1000','2025-02-23 11:09:21'),
(2,2,'900','2025-02-23 11:09:11'),
(3,4,'4000','2025-03-24 23:19:05');

/*Table structure for table `history` */

DROP TABLE IF EXISTS `history`;

CREATE TABLE `history` (
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `result` varchar(20) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`history_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `history` */

/*Table structure for table `laboratory` */

DROP TABLE IF EXISTS `laboratory`;

CREATE TABLE `laboratory` (
  `laboratory_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `path` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`laboratory_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `laboratory` */

insert  into `laboratory`(`laboratory_id`,`login_id`,`name`,`place`,`phone`,`email`,`path`) values 
(1,8,'lab1','ernakulam','1232323232','lab1@gmail.com','static/images/00b5bc19-dbb9-4a69-8300-7a61b21bd033imag222.jpg');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`user_type`) values 
(1,'admin','admin','admin'),


/*Table structure for table `payments` */

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

/*Data for the table `payments` */

insert  into `payments`(`payment_id`,`booking_id`,`date_time`,`status`) values 
(1,1,'2025-02-23 12:15:58','pending'),
(2,2,'2025-02-23 12:19:14','pending'),
(3,3,'2025-02-23 12:27:49','pending'),
(4,4,'2025-03-09 22:38:27','pending'),


/*Table structure for table `prediction` */

DROP TABLE IF EXISTS `prediction`;

CREATE TABLE `prediction` (
  `prediction_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`prediction_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `prediction` */

insert  into `prediction`(`prediction_id`,`user_id`,`result`,`date`) values 
(1,2,'Low Stroke Risk','2025-03-10'),
(2,2,'Low Stroke Risk','2025-03-10'),
(3,2,'Low Stroke Risk','2025-03-10'),
(4,2,'Low Stroke Risk','2025-03-10'),
(5,2,'Low Stroke Risk','2025-03-11'),
(6,2,'Low Stroke Risk','2025-03-11'),
(7,2,'Low Stroke Risk','2025-03-11'),
(8,2,'Low Stroke Risk','2025-03-11'),
(9,2,'Low Stroke Risk','2025-03-11'),
(10,2,'Low Stroke Risk','2025-03-11'),
(11,2,'Low Stroke Risk','2025-03-11'),
(12,2,'Low Stroke Risk','2025-03-11'),
(13,2,'Low Stroke Risk','2025-03-11'),
(14,2,'Low Stroke Risk','2025-03-11'),
(15,2,'Low Stroke Risk','2025-03-11'),
(16,2,'Low Stroke Risk','2025-03-11'),
(17,2,'Low Stroke Risk','2025-03-11'),
(18,2,'HIGH STROKE CONDITION','2025-03-11'),
(19,2,'LOW STROKE CONDITION','2025-03-11'),
(20,2,'Low Stroke Risk','2025-03-24');

/*Table structure for table `ratings` */

DROP TABLE IF EXISTS `ratings`;

CREATE TABLE `ratings` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `rate` varchar(10) DEFAULT NULL,
  `review` varchar(100) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `ratings` */

insert  into `ratings`(`rating_id`,`user_id`,`doctor_id`,`rate`,`review`,`date_time`) values 
(1,1,1,'2','good','2025-02-23 12:17:55'),
(2,1,1,'1.5','chvjh','2025-02-23 12:28:20'),
(3,2,2,'3','good','2025-03-10'),
(4,2,2,'4','nice ','2025-03-10'),
(5,2,2,'4','nice ','2025-03-10'),
(6,2,2,'4','nice ','2025-03-10'),
(7,2,2,'3','goodddddd\r\n','2025-03-24'),
(8,2,2,'3','goodddddd\r\n','2025-03-24');

/*Table structure for table `request` */

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `laboratory_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `file` varchar(1000) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `request` */

insert  into `request`(`request_id`,`laboratory_id`,`user_id`,`file`,`amount`,`date`,`status`) values 

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `house_name` varchar(20) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `path` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`user_id`,`login_id`,`first_name`,`last_name`,`house_name`,`place`,`phone`,`email`,`path`) values 


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

