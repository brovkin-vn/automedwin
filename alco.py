from datetime import datetime
import logging
import time
from unittest import result
# from pynput import keyboard
import log
import args
import threading
import serial

# DATA_LEN = 154

class Alco(threading.Thread):


    def __init__(self, log, port='COM3') -> None:
        super().__init__()
        # _args = args.Args()
        # self._log = log.Log()
        # self._log = self._log.getLogger('pump',level=logging.DEBUG if _args.enable_verbose else logging.INFO)
        self._log = log
        self._log.info(f'init alco device modul on {port=}')
        self._buffer = ''
        self._tick = datetime.now() 
        self._callback = None
        self._terminated = False
        self._ser = serial.Serial(port, 4800, timeout=1)
        self._data = ''


    def send_start_cmd(self):
        self._ser.flushInput()
        self._ser.flushOutput()
        self._ser.write('$START\n'.encode())
        self._ser.flushOutput()

    def run(self):
        while True:
            line = self._ser.readline()
            if len(line) > 0:
                self._buffer = line.decode()
                self._log.debug(f'read {self.buffer=}')
                result, self._data = self.parse(self.buffer)
                if result:
                    self._log.debug(f'{self.data=}')     
                    if self._callback:
                        self._callback(self.data)   
                    self._buffer = ''
            if self._terminated:
                break
        self._log.debug('stop run')

    def parse(self, data):
        self._log.debug(f'{data=}')
        if data.find('RESULT') > 0:
            alco_data = data[8:13]
            return True, alco_data
        else:
            return False, None
           

    @property
    def buffer(self):
        return self._buffer

    @property
    def data(self):
        return self._data
    

    def connect(self, foo):
        self._callback = foo
    
    def stop(self):
        self._terminated = True

    def test_callback(self, data):
        self._log.info(f'test callback, on_alco_data_is_ready, data:{data}')
        self.stop()
        exit()


def test():
    print('test pump')
    alco = Alco(log = log.Log().getLogger(name='test'), port='COM1')
    alco.connect(alco.test_callback)    
    alco.start()
    alco.send_start_cmd()
    n = 20
    for i in range(n):
        if alco.is_alive():
            break
        time.sleep(1)
        print(f'whait alco result  {n - i}...')
    alco.stop()
    
    

    

if __name__ == "__main__":
    test()
