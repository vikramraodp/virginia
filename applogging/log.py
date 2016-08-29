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
