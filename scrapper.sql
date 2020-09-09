CREATE TABLE `scrapper`(
 `link` varchar(800) COLLATE utf8_unicode_ci NULL,
 `source_link` varchar(800) COLLATE utf8_unicode_ci NOT NULL,
 `is_crawled` BOOLEAN NOT NULL DEFAULT FALSE,
 `last_crawl_date` timestamp NULL DEFAULT NULL,
 `response_status` int COLLATE utf8_unicode_ci NULL,
 `content_type` varchar(255) COLLATE utf8_unicode_ci NULL,
 `content_length` varchar(255) COLLATE utf8_unicode_ci  NULL,
 `filepath` varchar(255) COLLATE utf8_unicode_ci NULL,
 `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DELIMITER $$
CREATE TRIGGER checker
BEFORE INSERT ON `scrapper`
FOR EACH ROW
BEGIN
	SET NEW.`last_crawl_date` = IFNULL(NEW.`last_crawl_date`, NOW());
	SELECT MAX(last_crawl_date) INTO @time1 FROM scrapper WHERE link = @link_to_check LIMIT 1;
    SELECT is_crawled INTO @crawled FROM scrapper WHERE last_crawl_date = @time1 AND link = @link_to_check ORDER BY is_crawled DESC LIMIT 1;
	IF @time1 IS NOT NULL THEN
		SET @time2 = TIMEDIFF(@time1,NOW()-INTERVAL 24 HOUR);
		IF @time2 >= 0 AND @crawled IS TRUE THEN
			SET NEW.`is_crawled` = FALSE;
		END IF;
	END IF;
END;
$$
