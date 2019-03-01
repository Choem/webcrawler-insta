import io
import json
import os

from urllib.request import urlopen
from utils import chunk

class ImageDownloader:
    def __init__(self, project_id):
        self.project_id = project_id

        with open('data/%s/data.json' % (project_id), 'r') as file:
            self.data = json.load(file)


    def download(self):
        if not os.path.isdir('data/%s/images' % (self.project_id)):
            os.mkdir('data/%s/images' % (self.project_id))

        posts = chunk(self.data, 50)
        
        for index, post in enumerate(posts):
            print('Downloading %d images' % (len(post)))
            self._write_images(post)
            print('Progress %f' % (100/len(posts)*index + 1))


    def _write_images(self, posts):
        for post in posts:
            try:
                response = urlopen(post['display_url'])
                if response.getcode() == 200:
                    file = open('data/%s/images/%s.jpg' % (self.project_id, post['id']), 'wb')
                    file.write(response.read())
                    file.close()
            except:
                pass