/*
Navicat SQL Server Data Transfer

Source Server         : 250
Source Server Version : 110000
Source Host           : 192.168.1.250:1433
Source Database       : ccpspider
Source Schema         : dbo

Target Server Type    : SQL Server
Target Server Version : 110000
File Encoding         : 65001

Date: 2018-03-02 15:27:50
*/


-- ----------------------------
-- Table structure for stats_list
-- ----------------------------
DROP TABLE [dbo].[stats_list]
GO
CREATE TABLE [dbo].[stats_list] (
[spider_name] varchar(255) NULL ,
[downloader_request_bytes] varchar(255) NULL ,
[downloader_request_count] varchar(255) NULL ,
[downloader_request_method_count_GET] varchar(255) NULL ,
[downloader_response_bytes] varchar(255) NULL ,
[downloader_response_count] varchar(255) NULL ,
[downloader_response_status_count_200] varchar(255) NULL ,
[start_time] datetime2(7) NULL ,
[finish_time] datetime2(7) NULL ,
[finish_reason] varchar(255) NULL ,
[item_scraped_count] varchar(255) NULL ,
[log_count_DEBUG] varchar(255) NULL ,
[log_count_ERROR] varchar(255) NULL ,
[log_count_INFO] varchar(255) NULL ,
[log_count_WARNING] varchar(255) NULL ,
[request_depth_max] varchar(255) NULL ,
[response_received_count] varchar(255) NULL ,
[scheduler_dequeued_redis] varchar(255) NULL ,
[scheduler_enqueued_redis] varchar(255) NULL 
)


GO
