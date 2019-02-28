import time
import json
import io
import argparse

from crawler import InstagramCrawler
from images import ImageDownloader

        
def callback():
    with open('data.json', 'w') as file:
        json.dump(crawler.get_data, file)
    print('Finished writing to file')

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-e', '--email', required=True)
argument_parser.add_argument('-p', '--password', required=True)
args = vars(argument_parser.parse_args())

crawler = InstagramCrawler(args['email'], args['password'])
crawler.signIn()
crawler.crawl('https://www.instagram.com/graphql/query/?query_hash=1b84447a4d8b6d6d0426fefb34514485&variables=%7B%22id%22%3A%22224081233%22%2C%22first%22%3A10000%7D', callback)
crawler.shutdown()

image_downloader = ImageDownloader()
image_downloader.download()
