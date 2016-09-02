import json
import six
from os.path import isfile, join
from processors.processor_factory import ProcessorFactory

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


class Plot(object):

    def __init__(self, seed):
        super(Plot, self).__init__()
        configure_log(logging.DEBUG,__name__)

        self.seedDir = '/var/www/virginia/narrative/seed'
        self.__underlyingPlot = None

        if isinstance(seed, dict):
            self.__underlyingPlot = seed
        elif isinstance(seed, six.string_types):
            self.__underlyingPlot = self.__loadPlotfromSeed(seed)

        self._processor = None
        if 'processor' in self.__underlyingPlot:
            self._processor = ProcessorFactory.getProcessor(self.__underlyingPlot['processor'])
        else:
            self._processor = ProcessorFactory.getProcessor('stanford')

        self.__clear()


    def __clear(self):
        self._tokens = []
        self._ner = []
        self._pos = []
        self._resultset = {}

    def __loadPlotfromSeed(self,seed):
        seed_plot = None
        if not seed.endswith('.json'):
            seed += '.json'
        logger.debug(join(self.seedDir, seed))
        logger.debug(isfile(join(self.seedDir, seed)))
        if isfile(join(self.seedDir, seed)):
            with open(join(self.seedDir, seed)) as seed_file:
                seed_plot = json.load(seed_file)

        return seed_plot

    def valid(self):
        logger.debug(str(self.__underlyingPlot == None))
        if self.__underlyingPlot:
            # Note: it may be unreasonable to expect 'identification' in all cases
            if 'characters' in self.__underlyingPlot:
                if 'synesthesia' in self.__underlyingPlot or 'identification' in self.__underlyingPlot:
                    return True

        return False

    def processor(self):
        return self._processor

    def hasSynesthesia(self):
        return ('synesthesia' in self.__underlyingPlot)

    def hasIdentification(self):
        return ('identification' in self.__underlyingPlot)

    def all(self):
        all_list = []
        if self.valid():
            for idx,character in enumerate(self.__underlyingPlot['characters']):
                if self.hasIdentification() and self.hasSynesthesia():
                    tupl = (character,self.__underlyingPlot['identification'][idx],self.__underlyingPlot['synesthesia'][idx])
                elif self.hasIdentification():
                    tupl = (character,self.__underlyingPlot['identification'][idx],None)
                else:
                    tupl = (character,None,self.__underlyingPlot['synesthesia'][idx])
                all_list.append(tupl)

        return all_list
