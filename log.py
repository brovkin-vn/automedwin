from stat import filemode
import time
import logging
import logging.handlers
import os


class Log(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Log, cls).__new__(cls)
        return cls.instance

    def __init__(self, log_file='log', log_dir='./log') -> None:
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        log_file = os.path.join(log_dir, log_file)


        self.time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='S', interval=1, backupCount=0)
        self.time_handler.suffix = '%Y-%m-%d.log'

        self.stream_handler = logging.StreamHandler()

        # fmt = '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
        fmt = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        self.time_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)


    def getLogger(self, name='logger', level=logging.DEBUG):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(self.time_handler)
        logger.addHandler(self.stream_handler)
        
        return logger


def test():
    log1 = Log()
    log2 = Log()
    print(id(log1), log1)
    print(id(log2), log2)
    log1 = log1.getLogger('buka',level=logging.INFO)
    log2 = log2.getLogger('byka')
    for i in range(10):
        log1.info(f'text {i=}')
        log2.debug(f'text {i=}')

if __name__ == '__main__':
    test()