#!/usr/bin/env python

import sys
import os

sys.path.insert(0, '/var/www/virginia')

os.environ['JAVA_HOME']='/usr/lib/jvm/java-8-openjdk-amd64/'
os.environ['STANFORDTOOLSDIR']='/home/vagrant/stanfordnlp'
os.environ['CLASSPATH']='/home/vagrant/stanfordnlp/stanford-postagger-2015-12-09/stanford-postagger.jar:/home/vagrant/stanfordnlp/stanford-ner-2015-12-09/stanford-ner.jar:/home/vagrant/stanfordnlp/stanford-parser-full-2015-12-09/stanford-parser.jar:/home/vagrant/stanfordnlp/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
os.environ['STANFORD_MODELS']='/home/vagrant/stanfordnlp/stanford-postagger-2015-12-09/models:/home/vagrant/stanfordnlp/stanford-ner-2015-12-09/classifiers'

from virginia import monologue_svc as application
