from cgi import print_arguments
from datetime import datetime
import logging
import time
from pynput import keyboard
import log
import args

class Reader():

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Reader, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, log) -> None:
        # _args = args.Args()
        # self._log = log.Log()
        # self._log = self._log.getLogger('reader',level=logging.DEBUG if _args.enable_verbose else logging.INFO)
        self._log = log
        self._log.info(f'init card reader {id(self)}')
        self._buffer = ''
        self._tick = datetime.now() 
        self.listener = keyboard.Listener(on_press=self.on_press)
        self._callback = None

    def start(self):
        self.listener.start()

    @property
    def card(self):
        return self._card

    @property
    def buffer(self):
        return self._buffer

    def connect(self, foo):
        self._callback = foo
    
    def on_press(self, key):
        try:
            # print(f"{key.__dict__=}")
            tick = datetime.now()
            d = tick - self._tick
            self._tick = tick
            if ((d.days==0) and (d.seconds==0) and (d.microseconds < 80000)) or (len(self._buffer) == 0):
                self._buffer = self._buffer + chr(key.vk)
                # self._buffer = self._buffer + key.char
            else:
                self._buffer = chr(key.vk)
                # self._buffer = key.char

            # self._log.debug(f'{d.seconds=} {d.microseconds=} {self.buffer=}')
            if len(self._buffer) == 8:
                self._log.info(f'pass is read card={self._buffer}')
                self._card = self._buffer
                if self._callback:
                    self._callback(self.card)
            
            
            
        except AttributeError as e:
            self._log.error(e)




def test():
    print('test reader')
    reader = Reader()
    reader.connect(on_pass_is_read)    
    reader.start()
    n = 50
    for i in range(n):
        time.sleep(1)
        print(f'whait card or press "q" to exit {n - i}...')
        if 'q' in reader.buffer:
            exit()

def on_pass_is_read(card):
    print(f'test callback, on pass is read, card:{card}')

if __name__ == "__main__":
    test()
