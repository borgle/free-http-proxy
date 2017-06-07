CREATE DATABASE `proxy` CHARACTER SET utf8mb4;
CREATE USER 'proxy'@'%' IDENTIFIED BY 'proxy.Mysql.8'; 
GRANT ALL PRIVILEGES  ON `proxy`.* TO 'proxy'@'%';
FLUSH PRIVILEGES;

USE `proxy`;
CREATE TABLE `http` (
  `ip` varchar(35) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `lastcheck` datetime DEFAULT NULL,
  `failtimes` int(11) DEFAULT '0',
  `svtime` datetime DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `idx_unique` (`ip`,`port`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

