import time
from cfg import *
from utils import *
import concurrent.futures

if __name__ == "__main__":  
    while True:
        link_list.clear()
        n_workers = 5
        with concurrent.futures.ThreadPoolExecutor(max_workers = n_workers) as executor:
        	for address in to_crawl:
        		try:
        		    futures = executor.submit(crawler, address)
        		    return_value = futures.result()
        		    if return_value == 1:
        			    break
        		except:
        			pass
        to_crawl.clear()   
        to_crawl.extend(link_list)
        if len(to_crawl) == 0:
            print("All links crawled")
            to_crawl.append("https://flinkhub.com/")
        time.sleep(5)