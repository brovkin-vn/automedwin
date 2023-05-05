from datetime import datetime
import logging
import time
# from pynput import keyboard
import log
import args
import threading
import serial

DATA_LEN = 154

class Pump(threading.Thread):

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Pump, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, log, port='COM1') -> None:
        super().__init__()
        # _args = args.Args()
        # self._log = log.Log()
        # self._log = self._log.getLogger('pump',level=logging.DEBUG if _args.enable_verbose else logging.INFO)
        self._log = log
        self._log.info(f'init pressure device modelt on {port=}')
        self._buffer = ''
        self._tick = datetime.now() 
        self._callback = None
        self._terminated = False
        self._ser = serial.Serial(port, 9600, timeout=1)
        self._pump_data = {}

    def run(self):
        while True:
            s = self._ser.read(DATA_LEN)
            if len(s) > 0:
                self._buffer += s.decode()
                self._log.debug('read: {}'.format(len(s)))        
            if len(self._buffer) == DATA_LEN:
                self._pump_data = self.parse(self.buffer)
                self._log.info(f'{self._buffer.encode()}')     
                self._log.info(f'{self.pump_data=}')     
                if self._callback:
                    self._callback(self.pump_data)   
                self._buffer = ''
            if self._terminated:
                break
        self._log.debug('stop run')

    def parse(self, data):
        pump_data = {}
        pump_data['H'] = data[6:12].strip()     # head
        pump_data['E'] = data[30:32].strip()    # Error code 
        pump_data['S'] = data[34:37].strip()    # Systolic blood pressure
        pump_data['mean'] = data[39:42].strip() # Mean arterial blood pressure
        pump_data['D'] = data[44:47].strip()    # Diastolic blood pressure
        pump_data['P'] = data[49:52].strip()    # Pulse rate
        pump_data['L'] = data[58:61].strip()    # Maximum pulse amplitude
        pump_data['max'] = data[63:66].strip()  # Maximum pressure
        pump_data['A'] = data[68:70].strip()    # INB diagnosis of pulse arrhythmia
        pump_data['M'] = data[72:73].strip()    # body motion
        pump_data['T'] = data[79:81].strip()    # measurement time
        return pump_data
           

    @property
    def buffer(self):
        return self._buffer

    @property
    def pump_data(self):
        return self._pump_data
    

    def connect(self, foo):
        self._callback = foo
    
    def stop(self):
        self._terminated = True

def test():
    print('test pump')
    pump = Pump(log = log.Log().getLogger(name='test'), port='COM1')
    pump.connect(on_pump_data_is_ready)    
    pump.start()
    n = 5
    for i in range(n):
        time.sleep(1)
        print(f'whait pump result  {n - i}...')
    pump.stop()
    # pump.join()
    
    

def on_pump_data_is_ready(data):
    print(f'test callback, on_pump_data_is_ready, data:{data}')

if __name__ == "__main__":
    test()
