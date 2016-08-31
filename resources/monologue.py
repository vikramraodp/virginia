from flask import Flask, jsonify, request, abort, make_response, g, url_for
from flask.ext.restful import Api, Resource, reqparse, fields, marshal_with

from processors.stanford_processor import StanfordProcessor
from processors.textblob_processor import TextBlobProcessor
from narrative.plot import Plot

import time
import os
import json

import logging
logger = logging.getLogger(__name__)

def configure_log(level=None,name=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler('/var/www/virginia/logs/%s.log' % name,'w','utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)


class Monologue(Resource):

    def __init__(self):
        self.processor = StanfordProcessor()
        #self.processor = TextBlobProcessor()
        configure_log(logging.DEBUG,__name__)

    # post json data format is as follows
    # {
    #   "monologue" : "this is the statement that the user inputs",
    #   "seed" : "identifier of a pre-defined plot, as of now, if this is defined, the plot parameter is ignored"
    #   "plot" {
    #       "characters": "array of fields to resolve and hence characters of this plot",
    #       "identification": "what the system should recognize each character as. The no. of elements of this array should match the number of characters"
    #       "synesthesia": "what each character in this plot really stands for. The no. of elements of this array should match the number of characters"
    #   }
    # }
    def post(self):
        json_data = request.get_json(force=True)
        if self.__validatePostedData(json_data):
            if isinstance(json_data, list):
                results = []
                for elem in json_data:
                    plot = self.__generatePlot(elem)
                    if not plot or not plot.valid():
                        abort(422)
                    output = self.processor.process(plot, elem['monologue'])
                    results.append(output)
                response = make_response(json.dumps(results))
                response.headers['content-type'] = 'application/json; charset=utf-8'
                return response
            elif isinstance(json_data, dict):
                plot = self.__generatePlot(json_data)
                logger.debug(str(plot==None))
                if not plot or not plot.valid():
                    logger.error('Plot Valid - ' + str(plot.valid()))
                    abort(422)
                response = make_response(json.dumps(self.processor.process(plot, json_data['monologue'])))
                response.headers['content-type'] = 'application/json; charset=utf-8'
                return response

        abort(422)

    def __generatePlot(self, data):
        if 'seed' in data:
            return Plot(data['seed'])
        elif 'plot' in data:
            return Plot(data['plot'])

        return None


    def __validatePostedData(self, data):
        isValid = True
        if isinstance(data, list):
            for elem in data:
                if not self.__validatePostedData(elem):
                    isValid = False
                    break
        elif isinstance(data, dict):
            if 'monologue' in data:
                if not 'seed' in data:
                    if not 'plot' in data:
                        isValid = False

        return isValid
