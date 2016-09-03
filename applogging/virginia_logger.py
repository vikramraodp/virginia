import logging

class Logger:

    log = logging.getLogger(__name__)

    @staticmethod
    def getLogger():
        return Logger.log

    @staticmethod
    def init():
        Logger.log.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('/var/www/virginia/logs/virginia.log','w','utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
        file_handler.setFormatter(file_format)
        Logger.log.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_format)
        Logger.log.addHandler(console_handler)
