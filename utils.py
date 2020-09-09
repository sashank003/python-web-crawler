import random
import string
import requests
import MySQLdb
import re
from cfg import *
from bs4 import BeautifulSoup
import urllib.parse
from database import *


def file_name():
    characters = string.ascii_letters + string.digits
    name = "".join(random.choice(characters) for num in range(8))
    return name

def crawler(url):
    db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
    cursor = db.cursor()
    request = requests.get(url)
    status = int(request.status_code)
    content_type = request.headers['Content-Type']
    content_length = len(request.content)
    path = None
    flag = 0
    sql_last_crawl_date = check_last_crawl_date(url)
    cursor.execute(sql_last_crawl_date)
    
    if status == 200:
        search = re.search("text/html(.*)",content_type)
    	if search:
    		res = request.text
    		soup = BeautifulSoup(res, "html.parser")
    		code = soup.prettify() 
    		links = soup.find_all('a')
    		extension = '.html';
    		mode = 'w'
            en = 'not_bin'
        else:
    		code = request.content
    		extension = '.' + content_type
    		mode = 'wb'
            en = 'bin'
    	name = file_name()
        path = "files\\" + name + extension
        file = open('files\\{}'.format(name) + extension, mode, encoding = encod[en])
    	file.write(code)
    	file.close()
    elif status != 200:
    	sql_table_insert_not_200 = insert_into_table_not_200(url, status, content_type, content_length)
    	cursor.execute(sql_table_insert_not_200)
    	db.commit()
    	db.close()
    	return flag
    for i in range(len(links)):
        nested_link = links[i].get('href')
        if nested_link == None:
            continue
        s1 = re.search("javascript:;",nested_link)
        if s1 or len(nested_link) <= 2:
            continue
        nested_link = urllib.parse.urljoin(url, nested_link)
        s2 = re.search("http(.*)",nested_link)
        result =urllib.parse.urlparse(nested_link)
        if all([result.scheme, result.netloc]) and s2:
        	pass
        else:
        	continue
        sql_url_to_check_for_last_crawl = url_to_check_for_last_crawl(nested_link)
        cursor.execute(sql_url_to_check_for_last_crawl)
        sql_table_insert_200 = insert_into_table_200(nested_link, url,status, content_type, content_length, path)
        cursor.execute(sql_table_insert_200)
        db.commit()
        if status == 200:
        	link_list.append(nested_link)
        	if len(link_list) >= 5000:
        	    print('Maximum limit reached')
        	    flag = 1
        	    db.rollback()
        	    db.close()
        	    return flag
        else:
        	pass
        
    db.close()
    return flag
