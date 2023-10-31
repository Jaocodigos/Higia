import colorlog
import logging
import os

log_level = colorlog.DEBUG
loggers = {}
logging_dir = './logs'

try:
    if not os.path.exists(logging_dir):
        os.mkdir(logging_dir)
except Exception as e:
    exit("The log dir can't be created.Aborting..")


def prepare_logs(name):
    global log_level, loggers
    if loggers.get(name):
        return loggers[name]
    return set_global_log(name)


def set_global_log(name):

    log_format = colorlog.ColoredFormatter(
        f'%(log_color)s - %(levelname)s: %(name)s: %(message)s', log_colors={'DEBUG':    'cyan',
                                                                             'INFO':     'green',
                                                                             'WARNING':  'yellow',
                                                                             'ERROR':    'red',
                                                                             'CRITICAL': 'red,bg_white',
                                                                             })
    handler = colorlog.StreamHandler()
    handler.setFormatter(log_format)

    logger = colorlog.getLogger(f'Higia.{name}')
    logger.setLevel(log_level)

    log_file = logging.FileHandler(f'./logs/{name}.log', mode='a')
    log_file.setLevel(log_level)
    log_file.setFormatter(log_format)

    logger.addHandler(log_file)
    logger.addHandler(handler)
    loggers[name] = logger
    return logger
