from processors.stanford_processor import StanfordProcessor
from processors.textblob_processor import TextBlobProcessor
from processors.ctakes_processor import CTakesProcessor

class ProcessorFactory:

    processors = { 'stanford':StanfordProcessor, 'textblob':TextBlobProcessor, 'cTakes':CTakesProcessor }
    instances = {}

    @staticmethod
    def getProcessor(processor_type):
        processor = None
        if processor_type in ProcessorFactory.instances:
            return ProcessorFactory.instances[processor_type]
        else:
            if processor_type in ProcessorFactory.processors:
                processor = ProcessorFactory.processors[processor_type]()
                ProcessorFactory.instances[processor_type] = processor

        return processor
