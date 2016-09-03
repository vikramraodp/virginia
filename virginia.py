from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, Response

from flask_restful import Resource, Api

from resources.monologue import Monologue
from resources.plot import Plot
from utils.vision import VisionApi
from applogging.virginia_logger import Logger

import os
import uuid
import json

monologue_svc = Flask(__name__)
monologue_svc.config.from_pyfile('configuration/appconfig.py')

monologue_resources = Api(monologue_svc)
monologue_resources.add_resource(Monologue, '/monologue')
monologue_resources.add_resource(Plot, '/plot')

vision_api_client = VisionApi()

Logger.init()

@monologue_svc.route('/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        Logger.getLogger().info('received ocr request...')
        global vision_api_client
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        full_path = os.path.join(monologue_svc.config['UPLOAD_FOLDER'], f_name)
        file.save(full_path)
        Logger.getLogger().info('saved file to: ' + f_name)
        file_list = [full_path]
        annotated_text = ''
        try:
            annotated_text = vision_api_client.detect_text(file_list)
        except:
            Logger.getLogger().error("Error calling google")
        deciphered_text = ''
        if full_path in annotated_text:
            desc = annotated_text[full_path]
            if len(desc):
                deciphered_text = desc[0]['description']
                deciphered_text = deciphered_text.replace('\n',' ').replace('\r',' ').replace('\t',' ')
        return jsonify({'text':deciphered_text})

if __name__ == '__main__':
    monologue_svc.run(debug=True)
