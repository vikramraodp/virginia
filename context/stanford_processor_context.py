
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

class StanfordProcessorContext(object):

    def __init__(self):
        super(StanfordProcessorContext, self).__init__()
        self.__clear()
        configure_log(logging.DEBUG,__name__)

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

        logger.debug(all_list)
        return all_list
