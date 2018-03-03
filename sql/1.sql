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

Date: 2018-03-03 15:05:07
*/


-- ----------------------------
-- Table structure for ccp_xz_newslist_1
-- ----------------------------
DROP TABLE [dbo].[ccp_xz_newslist_1]
GO
CREATE TABLE [dbo].[ccp_xz_newslist_1] (
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
[libao] varchar(MAX) NULL ,
[yhtj_qt] varchar(255) NULL ,
[yhtj_dp] varchar(255) NULL ,
[yhtj_bz] varchar(MAX) NULL ,
[by_zbzq] varchar(255) NULL ,
[by_jlfy] varchar(255) NULL ,
[by_jyfy] varchar(255) NULL ,
[bx_gs] varchar(255) NULL ,
[bx_fy] varchar(255) NULL ,
[dk_jrgs] varchar(255) NULL ,
[dk_dkfs] varchar(255) NULL ,
[address] varchar(255) NULL ,
[tel] varchar(255) NULL ,
[srcsys] varchar(24) NOT NULL ,
[url] varchar(255) NULL ,
[updatetime] bigint NULL ,
[salesinfotype1] varchar(24) NULL ,
[sid] int NOT NULL IDENTITY(1,1) ,
[manufacture] varchar(24) NULL ,
[brandname] varchar(24) NULL ,
[match_flag] varchar(50) NULL 
)


GO
DBCC CHECKIDENT(N'[dbo].[ccp_xz_newslist_1]', RESEED, 211684611)
GO

-- ----------------------------
-- Indexes structure for table ccp_xz_newslist_1
-- ----------------------------
CREATE INDEX [idx_ccp_xz_newslist_1] ON [dbo].[ccp_xz_newslist_1]
([postdate] ASC, [salesinfoid] ASC) 
GO
CREATE INDEX [idx_ccp_xz_newslist_1_ag] ON [dbo].[ccp_xz_newslist_1]
([srcsys] ASC, [agencyid] ASC, [postdate] ASC) 
GO
CREATE INDEX [idx_ccp_xz_newslist_1_srcsys] ON [dbo].[ccp_xz_newslist_1]
([srcsys] ASC) 
GO
CREATE INDEX [sfid] ON [dbo].[ccp_xz_newslist_1]
([salesinfoid] ASC) 
GO

-- ----------------------------
-- Primary Key structure for table ccp_xz_newslist_1
-- ----------------------------
ALTER TABLE [dbo].[ccp_xz_newslist_1] ADD PRIMARY KEY ([salesinfoid], [srcsys])
GO
