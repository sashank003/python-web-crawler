def check_last_crawl_date(url):
	sql= 'SELECT MAX(created_at) INTO @last_crawl_date FROM scrapper WHERE source_link ="{}" AND is_crawled IS TRUE ORDER BY created_at DESC LIMIT 1'.format(url)
	return sql
def insert_into_table_not_200(url, status, content_type, content_length):
	sql = "INSERT INTO scrapper(source_link, is_crawled, last_crawl_date, response_status, content_type, content_length, created_at) VALUES ('{}', {}, {}, '{}', '{}', '{}', {})".format(url, 'TRUE', '@last_crawl_date', status, content_type, content_length, 'NOW()')
	return sql
def url_to_check_for_last_crawl(nested_link):
	sql = 'SELECT "{}" INTO @link_to_check'.format(nested_link)
	return sql

def insert_into_table_200(nested_link, url,status, content_type, content_length, path):
	sql = "INSERT INTO scrapper(link, source_link, is_crawled, last_crawl_date, response_status, content_type, content_length, filepath, created_at) VALUES ('{}', '{}', {}, {}, '{}', '{}', '{}', '{}', {})".format(nested_link, url, 'TRUE', '@last_crawl_date', status, content_type, content_length, path, 'NOW()')
	return sql
