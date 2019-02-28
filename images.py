import io
import json
import os

from urllib.request import urlopen 

class ImageDownloader:
    def __init__(self):
        with open('data.json', 'r') as file:
            self.data = json.load(file)


    def download(self):
        if not os.path.isdir('images'):
            os.mkdir('images')

        collections = self._chunk(self.data, 50)
        
        for index, collection in enumerate(collections):
            print('Downloading %d images' % (len(collection)))
            self._write_images(collection)
            print('Progress %f' % (100/len(collections)*index + 1))


    def _chunk(self, data, size):
        array = list()
        for i in range(0, len(data), size):
            array.append(data[i:i+size])
        return array


    def _write_images(self, images):
        for image in images:
            file = open('images/%s.jpg' % (image['id']), 'wb')
            try:
                file.write(urlopen(image['display_url']).read())
                file.close()
            except:
                pass