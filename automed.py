from wx import App  
from log import Log
from args import Args
from model import Model
from automat import Automat
from mainframe import MainFrame
from rest import Rest 
from reader2 import Reader
from pump import Pump
from alco import Alco
from piro import Piro

if __name__ == "__main__":
    log = Log().getLogger(name='automed')
    log.info('start automed app')

    args = Args()
    model = Model(log, args)
    rest = Rest(log)
    
    automat = Automat(log, model, rest)

    reader = Reader(log)
    # reader.connect(automat.on_card_data_is_ready)
    # reader.start()
    
    pump = Pump(log, args.pump_port)
    pump.connect(automat.on_pump_data_is_ready)
    pump.start()

    alco = None
    model.enable_alco = args.enable_alco
    if args.enable_alco:
        try:
            alco = Alco(log, args.alco_port)
            alco.connect(automat.on_alco_data_is_ready)
            alco.start()
            automat.connect_alco_start(alco.send_start_cmd)
        except Exception as e:
            log.error(e)
            model.enable_alco = False


    piro = None
    model.enable_piro = args.enable_piro
    if args.enable_piro:
        try:
            piro = Piro(log, args.piro_port)
            piro.connect(automat.on_piro_data_is_ready)
            piro.start()
        except Exception as e:
            log.error(e)
            model.enable_piro = False

    app = App()
    frame = MainFrame(None, 'Hello', log=log, model=model, args=args)
    frame.connect(automat.on_card_data_is_ready)
    frame.bindAutomat(automat)
    automat.start()
    frame.Show()

    app.MainLoop()

    pump.stop()
    if alco: alco.stop()
    if piro: piro.stop()
    automat.stop()
