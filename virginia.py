from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, Response

from flask_restful import Resource, Api

from resources.monologue import Monologue
from resources.plot import Plot

import logging
from logging.handlers import RotatingFileHandler

monologue_svc = Flask(__name__)
monologue_svc.config.from_pyfile('configuration/appconfig.py')

monologue_resources = Api(monologue_svc)
monologue_resources.add_resource(Monologue, '/monologue')
monologue_resources.add_resource(Plot, '/plot')

if __name__ == '__main__':
    handler = RotatingFileHandler('/var/www/virginia/logs/virginia.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    monologue_svc.logger.addHandler(handler)
    monologue_svc.run()
