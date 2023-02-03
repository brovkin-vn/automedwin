from wx import App  
from log import Log
from args import Args
from model import Model
from automat import Automat
from mainframe import MainFrame
from rest import Rest 
from reader import Reader
from pump import Pump
from alco import Alco
from piro import Piro

if __name__ == "__main__":
    log = Log().getLogger(name='automed')
    log.info('start automed app')

    args = Args()
    model = Model(log)
    rest = Rest(log)
    
    automat = Automat(log, args, model, rest)

    reader = Reader(log)
    reader.connect(automat.on_card_data_is_ready)
    reader.start()
    
    pump = Pump(log, args.pump_port)
    pump.connect(automat.on_pump_data_is_ready)
    pump.start()

    alco = Alco(log, args.alco_port)
    alco.connect(automat.on_alco_data_is_ready)
    alco.start()

    piro = Piro(log, args.piro_port)
    piro.connect(automat.on_piro_data_is_ready)
    piro.start()

    app = App()
    frame = MainFrame(None, 'Hello', log=log, model=model, args=args)
    frame.bindAutomat(automat)
    automat.start()
    frame.Show()
    app.MainLoop()

    pump.stop()
    alco.stop()
    piro.stop()
    automat.stop()
