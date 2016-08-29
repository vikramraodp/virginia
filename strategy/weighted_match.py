

class WeightedMatchStrategy(object):

    def __init__(self):
        super(WeightedMatchStrategy, self).__init__()
        self.__clear()

    def __clear(self):
        self._plot = None
        self._context = None

        self._pipeline = { 'found':[], 'remaining':[]}
        self._inputstack = []

    def apply(self, plot, context):
        self.__clear()

        self._plot = plot
        self._context = context

        self.__generatePipeline()
        self.__process()

        return self._pipeline['found']

    def __generatePipeline(self):
        self._pipeline['remaining'] = self._plot.all()
        self._inputstack = self._context.all()

    def __process(self):
        # one pass filter
        n = len(self._pipeline['remaining'])
        for idx in xrange(n):
            p = self._pipeline['remaining'][idx]
            pattern = (None,None,p[1],p[2])
            result = sorted(filter(lambda x: all(p is None or r == p for r, p in zip(x, pattern)),self._inputstack),key=lambda y:y[0])
            if len(result):
                new_match = {'for':self._pipeline['remaining'][idx][0],'match':result[0][1], 'possiblities':[r[1] for r in result[1:]]}
                self._pipeline['found'].append(new_match)
                self._inputstack = [(ord,tok,ner,pos) for ord,tok,ner,pos in self._inputstack if tok != result[0][1]]
