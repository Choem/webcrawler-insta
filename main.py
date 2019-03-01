import time
import json
import io
import argparse
import os
import shutil

from crawler import InstagramCrawler
from images import ImageDownloader
from vision import Vision

def callback():
    if not os.path.isdir('data'):
        os.mkdir('data')

    if os.path.isdir('data/%s' % (crawler.get_project_id)):
        shutil.rmtree('data/%s' % (crawler.get_project_id))

    if not os.path.isdir('data/%s' % (crawler.get_project_id)):
        os.mkdir('data/%s' % (crawler.get_project_id))

    with open('data/%s/data.json' % (crawler.get_project_id), 'w') as data:
        json.dump(crawler.get_data, data)
    print('Finished writing data to data/%s/data.json' % (crawler.get_project_id))

    with open('data/%s/location.json' % (crawler.get_project_id), 'w') as location:
        json.dump(crawler.get_location, location)
    print('Finished writing location to data/%s/location.json' % (crawler.get_project_id))      


start = time.time()

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-e', '--email', required=True)
argument_parser.add_argument('-p', '--password', required=True)
args = vars(argument_parser.parse_args())

crawler = InstagramCrawler(args['email'], args['password'])
crawler.signIn()
crawler.crawl('https://www.instagram.com/graphql/query/?query_hash=1b84447a4d8b6d6d0426fefb34514485&variables=%7B%22id%22%3A%22224081233%22%2C%22first%22%3A10000%7D', callback)
crawler.shutdown()

image_downloader = ImageDownloader(crawler.get_project_id)
image_downloader.download()

google_vision = Vision(crawler.get_project_id, 'ds41c-232407-bb6ea0813a31.json')
google_vision.process()

end = time.time()

print('Script executed in %f seconds' % (end - start))
