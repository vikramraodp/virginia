from applogging.virginia_logger import Logger

class StanfordProcessorContext(object):

    def __init__(self):
        super(StanfordProcessorContext, self).__init__()
        self.__clear()

    def __clear(self):
        self._tokens = []
        self._ner = []
        self._pos = []

    def __resolveToken(self,token):
        ner = next((n[1] for n in self._ner if n[0] == token),None)
        pos = next((p[1] for p in self._pos if p[0] == token),None)
        return ner,pos

    def create(self,tokens,ner,pos):
        self._tokens = tokens
        self._ner = ner
        self._pos = pos

    def all(self):
        all_list = []
        for idx,token in enumerate(self._tokens):
            ner,pos = self.__resolveToken(token)
            all_list.append((idx,token,ner,pos))

        Logger.getLogger().debug(all_list)
        return all_list
