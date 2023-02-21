from datetime import datetime
import logging
import time
from pynput import keyboard
import log
import args
import threading
import serial
import serial.tools.list_ports

DATA_LEN = 7

class Piro(threading.Thread):


    def __init__(self, log, port='COM3') -> None:
        super().__init__()
        self._log = log
        self._log.info(f'init pirometer device module on {port=}')
        self._buffer = ''
        self._tick = datetime.now() 
        self._callback = None
        self._terminated = False
        try:
            self._ser = serial.Serial(port, 115200, timeout=1)
        except:
            raise(Exception(f'Don`t open the pirometer port: {port}'))
        self._piro_data = 0

    def run(self):
        while True:
            s = self._ser.read(DATA_LEN)
            if len(s)>0:
                self._log.debug(f'read data {s=}')
            if len(s) == DATA_LEN:
                self._buffer = s
                self._piro_data = self.parse(s)
                self._log.info(f'{self._piro_data=}')
                if self._callback:
                    self._callback(self.piro_data)   
                self._buffer = ''
            if self._terminated:
                break
        self._log.debug('stop run')

    def parse(self, data):
        data = list(data)
        piro_data = ((data[5] << 8) + data[4]) / 10.0
        self._log.debug(f'{piro_data=}')
        return piro_data

    @property
    def buffer(self):
        return self._buffer

    @property
    def piro_data(self):
        return self._piro_data
    

    def connect(self, foo):
        self._callback = foo
    
    def stop(self):
        self._terminated = True

def test():
    print('test pirometer')
    ports = serial.tools.list_ports.comports()
    ports = [port for port in ports]
    print(f"{[port[0] for port in ports]}")
    piro = Piro(log = log.Log().getLogger(name='test'), port='COM8')
    piro.connect(on_piro_data_is_ready)    
    piro.start()
    n = 5
    for i in range(n):
        time.sleep(1)
        print(f'whait piro result  {n - i}...')
    piro.stop()
    
    

def on_piro_data_is_ready(data):
    print(f'test callback, on_piro_data_is_ready, data:{data}')

if __name__ == "__main__":
    test()
