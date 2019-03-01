import json
import os
import asyncio
import concurrent.futures

from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account

from base64 import encodebytes, encodestring, b64encode
from utils import chunk

class Vision:
    credentials = client = None
    features = []
    requests = []
    responses = []
    count = 0

    def __init__(self, project_id, private_key_file_path):
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(private_key_file_path)
        self.features = [
            {'type': vision_v1.enums.Feature.Type.LABEL_DETECTION},
            {'type': vision_v1.enums.Feature.Type.WEB_DETECTION}, 
            {'type': vision_v1.enums.Feature.Type.IMAGE_PROPERTIES},
            {'type': vision_v1.enums.Feature.Type.SAFE_SEARCH_DETECTION},
            {'type': vision_v1.enums.Feature.Type.OBJECT_LOCALIZATION},
            {'type': vision_v1.enums.Feature.Type.DOCUMENT_TEXT_DETECTION},
            {'type': vision_v1.enums.Feature.Type.TEXT_DETECTION},
            {'type': vision_v1.enums.Feature.Type.LANDMARK_DETECTION},
            {'type': vision_v1.enums.Feature.Type.LOGO_DETECTION},
            {'type': vision_v1.enums.Feature.Type.FACE_DETECTION},
        ]
        self.client = vision_v1.ImageAnnotatorClient(credentials=self.credentials)
        print('Initialized Google Vision API')

    def process(self):
        print('Processing images')
        with open('data/%s/data.json' % (self.project_id), 'rb') as data:
            posts = json.load(data)
            for post in posts:
                image_path = 'data/%s/images/%s.jpg' % (self.project_id, post['id'])

                if os.path.exists(image_path):
                    image = open(image_path, 'rb').read()

                    self.requests.append({ 
                        'image': { 'content': image },
                        'features': self.features 
                    })

        print('Chunking...')        
        requests = chunk(self.requests, 10)
        batches = chunk(requests, 20)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            {executor.submit(self._process_batch, batch): batch for batch in batches}
                
    def _process_batch(self, batch):
        for images in batch:
            response = self.client.batch_annotate_images(requests=images)
            self.count += len(images)
            print('images %d/%d' % (self.count, len(self.requests)))
            self.responses.extend(response.responses)
            
        
vision = Vision('224081233', 'ds41c-232407-bb6ea0813a31.json')
vision.process()
