import requests
import json
import ConfigParser

from context.stanford_processor_context import StanfordProcessorContext
from strategy.aggregated_match import AggregatedMatchStrategy

class CTakesAdvancedProcessor:

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
        self.__svcURL += 'clinicalv2'

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
                tags = tags + self.__extractClassification(annotation)
        return tags

    def __extractClassification(self, annotationObj):
        tags = []
        tag = self.__extractFeature('signsAndSymptoms', 'SignsAndSymptoms', annotationObj)
        if tag:
            tags.append(tag)
        tag = self.__extractFeature('findings', 'Findings', annotationObj)
        if tag:
            tags.append(tag)
        tag = self.__extractFeature('measurement', 'Measurement', annotationObj)
        if tag:
            tags.append(tag)
        tag = self.__extractFeature('labEvents', 'LabEvents', annotationObj)
        if tag:
            tags.append(tag)
        tag = self.__extractFeature('medications', 'Medications', annotationObj)
        if tag:
            tags.append(tag)
        tag = self.__extractFeature('procedures', 'Procedures', annotationObj)
        if tag:
            tags.append(tag)

        medical_history = self.__extractNestedClassification('MedicalHistory',annotationObj['medicalHistory'])
        family_history = self.__extractNestedClassification('FamilyHistory',annotationObj['familyHistory'])

        tags = tags + medical_history + family_history
        return tags

    def __extractNestedClassification(self, annotationType, annotationObj):
        nested_list = []
        tag = self.__extractFeature('signsAndSymptoms', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        tag = self.__extractFeature('findings', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        tag = self.__extractFeature('measurement', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        tag = self.__extractFeature('labEvents', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        tag = self.__extractFeature('medications', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        tag = self.__extractFeature('procedures', annotationType, annotationObj)
        if tag:
            nested_list.append(tag)
        return nested_list

    def __extractFeature(self, key, annotationType, annotationObj):
        if not key in annotationObj:
            return None

        value = annotationObj[key];
        if len(value):
            self._tokens.append(value)
            return (value, annotationType)
        else:
            return None

    def __updateprocessorContext(self):
        entities = self._tagEntities()
        self._context.create(self._tokens,entities,[])

    def process(self, plot, monologue):
        self.__processingPreflight(monologue)
        self.result['out'] = self._strategy.apply(plot,self._context)
        return self.result
