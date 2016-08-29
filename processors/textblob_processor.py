from context.stanford_processor_context import StanfordProcessorContext
from strategy.weighted_match import WeightedMatchStrategy

#from nltk.tag import StanfordNERTagger
from textblob import TextBlob as tb
from textblob_aptagger import PerceptronTagger
from nltk.tag import StanfordNERTagger
import nltk

class TextBlobProcessor:

    def __init__(self):
        self.nerTagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
        self.posTagger = PerceptronTagger()
        self._context = StanfordProcessorContext()
        self._strategy = WeightedMatchStrategy()
        nltk.data.path.append('/var/www/virginia/nltk_data/')

    def __processingPreflight(self, monologue):
        self.result = {}
        self.result['in'] = monologue
        self.result['out'] = None
        self.tokens = monologue.split()
        self.monologue = monologue

        self.__updateprocessorContext()

    def _tagEntities(self):
        return self.nerTagger.tag(self.tokens)
        #return self.nerTagger.tag(text.split())

    def _tagPartOfSpeech(self):
        posTags = tb(self.monologue,pos_tagger=self.posTagger)
        return posTags.tags
        #return self.posTagger.tag(text.split())

    def __updateprocessorContext(self):
        self._context.create(self.tokens,self._tagEntities(),self._tagPartOfSpeech())

    def process(self, plot, monologue):
        self.__processingPreflight(monologue)

        self.result['out'] = self._strategy.apply(plot,self._context)

        return self.result
