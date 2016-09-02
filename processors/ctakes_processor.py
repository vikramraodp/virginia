import requests
import json
import ConfigParser

from context.stanford_processor_context import StanfordProcessorContext
from strategy.aggregated_match import AggregatedMatchStrategy

class CTakesProcessor:

    def __init__(self):
        self._context = StanfordProcessorContext()
        self._strategy = AggregatedMatchStrategy()
        self.__loadConfiguration()

    def __loadConfiguration(self):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'/var/www/virginia/configuration/config.ini'
        configParser.read(configFilePath)
        self.__svcURL = configParser.get('taggerservice','baseURL')
        if not self.__svcURL.endswith('/'):
            self.__svcURL += '/'
        self.__svcURL += 'clinical'

    def __processingPreflight(self, monologue):
        self.result = {}
        self.result['in'] = monologue
        self.result['out'] = None
        self._tokens = []

        self.__updateprocessorContext()

    def _tagEntities(self):
        data = {'monologue': self.result['in']}
        headers = {'Content-Type':'application/json', 'Accept':'application/json'}
        r = requests.post(url = self.__svcURL, headers = headers, data = json.dumps(data))
        tags = []
        if r.status_code == 200:
            annotatedData = r.json()
            for annotation in annotatedData:
                word = annotation['word']
                if 'extras' in annotation:
                    if 'preferredText' in annotation['extras']:
                        if len(annotation['extras']['preferredText']):
                            word = annotation['extras']['preferredText']
                self._tokens.append(word)
                tags.append((word,annotation['annotation']))
        return tags

    def __updateprocessorContext(self):
        entities = self._tagEntities()
        self._context.create(self._tokens,entities,[])

    def process(self, plot, monologue):
        self.__processingPreflight(monologue)
        self.result['out'] = self._strategy.apply(plot,self._context)
        return self.result
