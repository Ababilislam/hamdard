CREATE TABLE IF NOT EXISTS `target_vs_achievement_route_item` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `first_date` date DEFAULT NULL,
  `target_date` date DEFAULT NULL,
  `item_id` varchar(10) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `price` double NOT NULL DEFAULT '0',
  `zone_id` varchar(50) NOT NULL DEFAULT '',
  `region_id` varchar(100) DEFAULT NULL,
  `area_id` varchar(20) DEFAULT NULL,
  `territory_id` varchar(100) DEFAULT NULL,
  `depot_id` varchar(10) DEFAULT NULL,
  `target_qty` int(11) DEFAULT NULL,
  `achievement_qty` int(11) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `target_vs_achievement_route_item`
--
ALTER TABLE `target_vs_achievement_route_item`
  ADD PRIMARY KEY (`id`), ADD KEY `cid` (`cid`,`first_date`,`territory_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `target_vs_achievement_route_item`
--
ALTER TABLE `target_vs_achievement_route_item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=0;