from bs4 import BeautifulSoup
from requests import get
import os


class Scraper(object):
    def load_images_from_thread(self, threadid):
        thread_request = get('http://boards.4chan.org/b/thread/' + threadid)

        thread_soup = BeautifulSoup(thread_request.text)
        image_links = thread_soup.select('.fileText a')

        folder_name = threadid
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        for index, image_link in enumerate(image_links):
            image_url = image_link.get('href')
            if image_url[:5] != 'http:':
                image_url = 'http:' + image_url

            image_request = get(image_url)

            if image_request.status_code in (200, 304):
                filename = image_url.split('/')[-1]
                file_path = os.path.abspath(os.path.join(folder_name, filename))

                print 'Scraping ' + str(index + 1) + '/' + str(len(image_links)) + ' from thread ' + threadid + '. Local filename: ' + filename

                with open(file_path, 'wb') as output:
                    output.write(image_request.content)

    def parse_thread_ids(self, threads):
        for index, thread_id in enumerate(threads):
            parsed_thread_id = thread_id.get('id')[1:] # removes first strange 't' character of thread ID
            self.load_images_from_thread(parsed_thread_id)

    def start(self):
        for i in xrange(7):
            url = 'http://boards.4chan.org/b/' + str(i+2)
            print('Currently parsing ' + url)
            thread_request = get(url)
            if thread_request.status_code != 200:
                raise Exception('Thread URL not found')

            thread_soup = BeautifulSoup(thread_request.text)
            threads = thread_soup.select('.thread')
            self.parse_thread_ids(threads)

if __name__ == '__main__':
    Scraper().start()