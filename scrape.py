from bs4 import BeautifulSoup
from requests import get
import os
import time
import sys


class Scraper(object):
    def load_images_from_thread(self, boardname, threadid):
        thread_request = get('http://boards.4chan.org/' + boardname + '/thread/' + threadid)

        thread_soup = BeautifulSoup(thread_request.text)
        image_links = thread_soup.select('.fileText a')

        folder_name = boardname
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for index, image_link in enumerate(image_links):
            image_url = image_link.get('href')
            if image_url[:5] != 'http:':
                image_url = 'http:' + image_url

            filename = image_url.split('/')[-1]
            file_path = os.path.abspath(os.path.join(folder_name, filename))
            if file_path.endswith('webm'):
                #print('Skipping .webm file: ' + file_path)
                return

            # skipping already downloaded images
            if not os.path.isfile(file_path):
                image_request = get(image_url)
                if image_request.status_code in (200, 304):
                    print 'Scraping /' + boardname + '/ ' + str(index + 1) + '/' + str(len(image_links)) + ' from thread ' + threadid + '. Local filename: ' + filename

                    with open(file_path, 'wb') as output:
                        output.write(image_request.content)

    def parse_thread_ids(self, threads, boardname):
        for index, thread_id in enumerate(threads):
            # removes first strange 't' character of thread ID from parsed html
            parsed_thread_id = thread_id.get('id')[1:]
            self.load_images_from_thread(boardname, parsed_thread_id)

    def start(self, boardname):
        for i in xrange(7):
            url = 'http://boards.4chan.org/' + boardname + '/' + str(i+2)
            print('Currently parsing ' + url)
            thread_request = get(url)
            if thread_request.status_code != 200:
                raise Exception('Thread URL not found')

            thread_soup = BeautifulSoup(thread_request.text)
            threads = thread_soup.select('.thread')
            self.parse_thread_ids(threads, boardname)

if __name__ == '__main__':
    board_name = sys.argv[1]
    while True:
        Scraper().start(board_name)
