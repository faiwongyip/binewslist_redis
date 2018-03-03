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

Date: 2018-03-03 15:05:39
*/


-- ----------------------------
-- Table structure for saleInfoContent
-- ----------------------------
DROP TABLE [dbo].[saleInfoContent]
GO
CREATE TABLE [dbo].[saleInfoContent] (
[salesinfoid] int NOT NULL ,
[mentioncar] varchar(255) NOT NULL ,
[oneclassify] varchar(24) NOT NULL ,
[twoclassify] varchar(24) NOT NULL ,
[content] varchar(255) NOT NULL ,
[note] varchar(500) NOT NULL ,
[srcsys] varchar(24) NOT NULL 
)


GO

-- ----------------------------
-- Indexes structure for table saleInfoContent
-- ----------------------------
CREATE INDEX [saleInfoContent_idx] ON [dbo].[saleInfoContent]
([salesinfoid] ASC, [srcsys] ASC) 
GO

-- ----------------------------
-- Primary Key structure for table saleInfoContent
-- ----------------------------
ALTER TABLE [dbo].[saleInfoContent] ADD PRIMARY KEY ([salesinfoid], [twoclassify], [content], [note])
GO
