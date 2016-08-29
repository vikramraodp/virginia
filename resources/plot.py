from flask import Flask, jsonify, request, abort, make_response, g, url_for
from flask.ext.restful import Api, Resource, reqparse, fields, marshal_with
from os import listdir
from os.path import isfile, join, basename,splitext
import json

class Plot(Resource):

    def __init__(self):
        self.plotDir = '/var/www/virginia/plot/seed'

    def get(self):
        plots = [splitext(basename(plot))[0] for plot in listdir(self.plotDir) if (isfile(join(self.plotDir, plot)) and plot.endswith(".json"))]
        return json.dumps(plots)
