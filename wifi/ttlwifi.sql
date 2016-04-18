/*
Navicat MySQL Data Transfer

Source Server         : host
Source Server Version : 50527
Source Host           : localhost:3306
Source Database       : ttlwifi

Target Server Type    : MYSQL
Target Server Version : 50527
File Encoding         : 65001

Date: 2016-04-17 09:50:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `keydata`
-- ----------------------------
DROP TABLE IF EXISTS `keydata`;
CREATE TABLE `keydata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `ssid` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `createtime` varchar(24) NOT NULL,
  `country` varchar(20) NOT NULL,
  `province` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `isp` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6970 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of keydata
-- ----------------------------

-- ----------------------------
-- Table structure for `keydatatmp`
-- ----------------------------
DROP TABLE IF EXISTS `keydatatmp`;
CREATE TABLE `keydatatmp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `ssid` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `createtime` varchar(24) NOT NULL,
  `country` varchar(20) DEFAULT NULL,
  `province` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `isp` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of keydatatmp
-- ----------------------------
