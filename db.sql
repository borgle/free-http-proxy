CREATE TABLE `http` (
  `ip` varchar(35) CHARACTER SET utf8 DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `lastcheck` datetime DEFAULT NULL,
  `failtimes` int(11) DEFAULT '0',
  `svtime` datetime DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `idx_unique` (`ip`,`port`),
  KEY `idx_checktime` (`lastcheck`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
