from context.stanford_processor_context import StanfordProcessorContext
from strategy.weighted_match import WeightedMatchStrategy

import requests
import json

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

    def __processingPreflight(self, monologue):
        self.result = {}
        self.result['in'] = monologue
        self.result['out'] = None
        self.tokens = nltk.word_tokenize(monologue)

        self.__updateprocessorContext()

    def _tagEntities(self):
        data = {'monologue': self.result['in']}
        headers = {'Content-Type':'application/json', 'Accept':'application/json'}
        r = requests.post(url = 'http://localhost:8080/taggerservice/ner', headers = headers, data = json.dumps(data))
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
        r = requests.post(url = 'http://localhost:8080/taggerservice/pos', headers = headers, data = json.dumps(data))
        tags = []
        if r.status_code == 200:
            annotatedData = r.json()
            for annotation in annotatedData:
                tags.append((annotation['word'],annotation['annotation']))
        return tags
        #return self.posTagger.tag(self.tokens)
        #return self.posTagger.tag(text.split())

    def __updateprocessorContext(self):
        self._context.create(self.tokens,self._tagEntities(),self._tagPartOfSpeech())

    def process(self, plot, monologue):
        self.__processingPreflight(monologue)

        self.result['out'] = self._strategy.apply(plot,self._context)

        return self.result
