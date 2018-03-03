/*
Navicat SQL Server Data Transfer

Source Server         : ali250
Source Server Version : 130000
Source Host           : rm-wz9n7u2xg45ub40qv0o.sqlserver.rds.aliyuncs.com,3433:1433
Source Database       : ccpspider
Source Schema         : dbo

Target Server Type    : SQL Server
Target Server Version : 130000
File Encoding         : 65001

Date: 2018-03-03 15:05:22
*/


-- ----------------------------
-- Table structure for ccp_xz_newslist_hd
-- ----------------------------
DROP TABLE [dbo].[ccp_xz_newslist_hd]
GO
CREATE TABLE [dbo].[ccp_xz_newslist_hd] (
[city] varchar(24) NULL ,
[agencyid] int NULL ,
[agencyname] varchar(255) NULL ,
[carsseriesid] int NULL ,
[carsseries_en] varchar(255) NULL ,
[carsseriesname] varchar(255) NULL ,
[salesinfoid] int NOT NULL ,
[salesinfotype] varchar(24) NULL ,
[title] varchar(255) NULL ,
[postdate] int NULL ,
[salesinfotype1] varchar(255) NULL ,
[keyword] varchar(255) NULL ,
[shijian] varchar(120) NULL ,
[changneiwai] varchar(120) NULL ,
[content] varchar(MAX) NULL ,
[address] varchar(255) NULL ,
[tel] varchar(255) NULL ,
[srcsys] varchar(24) NOT NULL ,
[url] varchar(255) NULL ,
[updatetime] bigint NULL ,
[sid] int NOT NULL IDENTITY(1,1) ,
[brandname] varchar(24) NULL ,
[manufacture] varchar(24) NULL 
)


GO
DBCC CHECKIDENT(N'[dbo].[ccp_xz_newslist_hd]', RESEED, 1284903)
GO

-- ----------------------------
-- Indexes structure for table ccp_xz_newslist_hd
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table ccp_xz_newslist_hd
-- ----------------------------
ALTER TABLE [dbo].[ccp_xz_newslist_hd] ADD PRIMARY KEY ([salesinfoid], [srcsys])
GO
