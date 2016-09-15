from context.stanford_processor_context import StanfordProcessorContext
from strategy.weighted_match import WeightedMatchStrategy

from applogging.virginia_logger import Logger

import requests
import json
import ConfigParser
import itertools
# from nltk.tag.stanford import StanfordPOSTagger
# from nltk.tag import StanfordNERTagger
# from nltk.parse.stanford import StanfordParser
# from nltk.parse.stanford import StanfordDependencyParser
import nltk

class StanfordProcessor:

    def __init__(self):
        #self.nerTagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
        #self.posTagger = StanfordPOSTagger('english-bidirectional-distsim.tagger')
        nltk.data.path.append('/var/www/virginia/nltk_data/')
        self._context = StanfordProcessorContext()
        self._strategy = WeightedMatchStrategy()
        self.__loadConfiguration()

    def __loadConfiguration(self):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r'/var/www/virginia/configuration/config.ini'
        configParser.read(configFilePath)
        baseURL = configParser.get('taggerservice','baseURL')
        if not baseURL.endswith('/'):
            baseURL += '/'
        self.__nerSvcURL = baseURL + 'ner'
        self.__posSvcURL = baseURL + 'pos'

    def __processingPreflight(self, monologue):
        self.result = {}
        self.result['in'] = monologue
        self.result['out'] = None
        #self.tokens = nltk.word_tokenize(monologue)
        self.__generateTokens(monologue)

        self.__updateprocessorContext()

    def __generateTokens(self, monologue):
        self.tokens = nltk.word_tokenize(monologue)
        self.tokens = self.tokens + list(itertools.chain.from_iterable([t.split('-') for t in self.tokens if '-' in t]))

    def _tagEntities(self):
        data = {'monologue': self.result['in']}
        headers = {'Content-Type':'application/json', 'Accept':'application/json'}
        r = requests.post(url = self.__nerSvcURL, headers = headers, data = json.dumps(data))
        tags = []
        if r.status_code == 200:
            annotatedData = r.json()
            for annotation in annotatedData:
                tags.append((annotation['word'],annotation['annotation']))
        return tags
        #return self.nerTagger.tag(self.tokens)
        #return self.nerTagger.tag(text.split())

    def _tagPartOfSpeech(self):
        data = {'monologue': self.result['in']}
        headers = {'Content-Type':'application/json', 'Accept':'application/json'}
        r = requests.post(url = self.__posSvcURL, headers = headers, data = json.dumps(data))
        tags = []
        if r.status_code == 200:
            annotatedData = r.json()
            for annotation in annotatedData:
                tags.append((annotation['word'],annotation['annotation']))
        return tags
        #return self.posTagger.tag(self.tokens)
        #return self.posTagger.tag(text.split())

    def __updateprocessorContext(self):
        #self._context.create(self.tokens,self._tagEntities(),self._tagPartOfSpeech())
        self._context.create(self.tokens,self._tagEntities(),[])

    def process(self, plot, monologue):
        Logger.getLogger().debug(monologue)
        self.__processingPreflight(monologue)
        self.result['out'] = self._strategy.apply(plot,self._context)
        return self.result
