from google.cloud import vision

class Vision:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()