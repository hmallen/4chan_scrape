from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from sys import argv
import os


def rn():
    return str(datetime.now()).replace(' ', '_')

url = argv[1]
thread_request = get(url)
if thread_request.status_code != 200:
    raise Exception('Thread URL not found')

thread_soup = BeautifulSoup(thread_request.text)

image_links = thread_soup.select('.fileText a')

folder_name = rn()
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for index, image_link in enumerate(image_links):

    print 'Scraping ' + str(index + 1) + '/' + str(len(image_links))

    image_url = image_link.get('href')
    if image_url[:5] != 'http:':
        image_url = 'http:' + image_url
    image_request = get(image_url)

    if image_request.status_code in (200, 304):

        content_type = image_request.headers['content-type']
        extension = ''
        if 'png' in content_type:
            extension = 'png'
        elif ('jpg' in content_type) or ('jpeg' in content_type):
            extension = 'jpg'
        elif 'gif' in content_type:
            extension = 'gif'

        filename = rn() + '.' + extension
        file_path = os.path.abspath(os.path.join(folder_name, filename))

        with open(file_path, 'wb') as output:
            output.write(image_request.content)
