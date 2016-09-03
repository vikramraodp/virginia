import base64
import os
import sys
import time

from googleapiclient import discovery
from googleapiclient import errors
import httplib2
from oauth2client.client import GoogleCredentials

from applogging.virginia_logger import Logger

class VisionApi(object):

    def __init__(self):
        credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build('vision', 'v1', credentials=credentials)
        self.log = Logger.getLogger()

    def detect_text(self, input_filenames, num_retries=3, max_results=6):
        batch_request = []
        for filename in input_filenames:
            request = {
                'image': {},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }]
            }

            if filename.startswith('gs://'):
                request['image']['source'] = {
                    'gcsImageUri': filename
                }
            else:
                with open(filename, 'rb') as image_file:
                    request['image']['content'] = base64.b64encode(
                        image_file.read()).decode('UTF-8')

            batch_request.append(request)

        request = self.service.images().annotate(
            body={'requests': batch_request})

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}

            text_response = {}
            for filename, response in zip(
                    input_filenames, responses['responses']):

                if 'error' in response:
                    log.error('API Error for {}: {}'.format(
                        filename,
                        response['error'].get('message', '')))
                    continue

                text_response[filename] = response.get('textAnnotations', [])

            return text_response

        except errors.HttpError as e:
            log.error('Http Error for {}: {}'.format(filename, e))
        except KeyError as e2:
            log.error('Key error: {}'.format(e2))
