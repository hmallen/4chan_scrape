from bs4 import BeautifulSoup
from requests import get
import os
import time
import sys


class Scraper(object):
    def scrape(self, url, folder_name):
        source_html = get(url)
        if source_html.status_code != 200:
            raise Exception('Thread URL not found')

        thread_soup = BeautifulSoup(source_html.text)
        original_image_links = thread_soup.select('.description')

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for link in original_image_links:
            original_image_url = 'http://' + link.contents[0]
            filename = original_image_url.split('/')[-1]
            file_path = os.path.abspath(os.path.join(folder_name, filename))
            if not os.path.isfile(file_path):
                image_request = get(original_image_url)
                if image_request.status_code in (200, 304):

                    print('Downloading image from ' + original_image_url)
                    #print 'Scraping /' + boardname + '/ ' + str(index + 1) + '/' + str(len(image_links)) + ' from thread ' + threadid + '. Local filename: ' + filename

                    with open(file_path, 'wb') as output:
                        output.write(image_request.content)
            else:
                print('Skipping file ' + original_image_url)

if __name__ == '__main__':
    s = Scraper()
    for i in xrange(100):
        url = 'http://www.ffffound.com/?offset=' + str(i*25) + '&'
        s.scrape(url, 'ffffound_images')