from asyncio.windows_events import NULL
import threading
import queue
import time

import log
from args import Args
from rest import Rest
from model import Model
from model import EVENTS 
from model import EVENT
from model import STATE 
from mainframe import MainFrame

class Automat(threading.Thread):


    def __init__(self, log, args, model:Model, rest:Rest) -> None:
        super().__init__()
        self.args:Args = args
        self.model = model
        self.rest = rest
        self.frame:MainFrame = NULL
        self._log = log
        self._log.info(f'init automat')
        self._terminated = False
        self._queue = queue.Queue()

    def do_step(self, event):

        match self.model.state:
            case STATE.START:
                # self.frame.showPanel(self.frame.panelErro)
                # self.model.state = STATE.START
                self.model.state = STATE.POST
                self.frame.showPanel(self.frame.panelPost)
            case STATE.POST:
                match event:
                    case EVENT.TEST:
                        self.model.state = STATE.TEST
                        self.model.timer_test = 0
                        self.frame.showPanel(self.frame.panelTest)
                    case EVENT.CARD:
                        self.frame.showPanel(self.frame.panelWait)
                        data = self.rest.get_full_name_by_card(card=self.model.card, box_id=self.model.box_id)
                        self.model.set_card_data(data)
                        result = data[0]
                        if result:
                            self.model.state = STATE.PUMP
                            self.model.timer_pump = 0
                            self.frame.showPanel(self.frame.panelPump)
                        else:
                            self.model.state = STATE.ERROR
                            self.model.timer_error = 0
                            # self.model.last_error_message = data[]
                            self.frame.showPanel(self.frame.panelErro)
                        
                    
            case STATE.TEST:
                match event:
                    case EVENT.CANCEL | EVENT.TIMER_TEST:
                        self.model.state = STATE.POST
                        self.model.timer_test = 0
                        self.frame.showPanel(self.frame.panelPost)
                    case EVENT.TIMER:
                        self.model.timer_test += 1
                        if self.model.is_timer_test:
                            self.put_event(EVENT.TIMER_TEST)
        
            case STATE.ERROR:
                match event:
                    case EVENT.CANCEL | EVENT.TIMER_ERROR:
                        self.model.state = STATE.POST
                        self.model.timer_error = 0
                        self.frame.showPanel(self.frame.panelPost)
                    case EVENT.TIMER:
                        self.model.timer_error += 1
                        if self.model.is_timer_error:
                            self.put_event(EVENT.TIMER_ERROR)
        
            case STATE.PUMP:
                match event:
                    case EVENT.PUMP:
                            if self.args.enable_piro:
                                self.model.state = STATE.PIRO
                                self.model.timer_piro = 0
                                self.frame.showPanel(self.frame.panelPiro)
                            elif self.args.enable_alco:
                                self.model.state = STATE.ALCO
                                self.model.timer_alco = 0
                                self.frame.showPanel(self.frame.panelAlco)
                            else:
                                self.save_pump_data()
                                self.model.state = STATE.SAVE
                                self.model.timer_save = 0
                                self.frame.showPanel(self.frame.panelSave)
                    case EVENT.CANCEL | EVENT.TIMER_PUMP:
                        self.model.state = STATE.POST
                        self.model.timer_pump = 0
                        self.frame.showPanel(self.frame.panelPost)
                    case EVENT.TIMER:
                        self.model.timer_pump += 1
                        if self.model.is_timer_pump:
                            self.put_event(EVENT.TIMER_PUMP)
                    case EVENT.ERROR:
                            self.model.state = STATE.ERROR
                            self.model.timer_error = 0
                            self.frame.showPanel(self.frame.panelErro)


            case STATE.PIRO:
                match event:
                    case EVENT.PIRO:
                            if self.args.enable_alco:
                                self.model.state = STATE.ALCO
                                self.model.timer_alco = 0
                                self.frame.showPanel(self.frame.panelAlco)
                            else:
                                self.save_pump_data()
                                self.model.state = STATE.SAVE
                                self.model.timer_save = 0
                                self.frame.showPanel(self.frame.panelSave)
                    case EVENT.CANCEL | EVENT.TIMER_PIRO:
                        self.model.state = STATE.POST
                        self.model.timer_piro = 0
                        self.frame.showPanel(self.frame.panelPost)
                    case EVENT.TIMER:
                        self.model.timer_piro += 1
                        if self.model.is_timer_piro:
                            self.put_event(EVENT.TIMER_PIRO)
                    case EVENT.ERROR:
                            self.model.state = STATE.ERROR
                            self.model.timer_error = 0
                            self.frame.showPanel(self.frame.panelErro)


            case STATE.ALCO:
                match event:
                    case EVENT.ACLO:
                        self.save_pump_data()
                        self.model.state = STATE.SAVE
                        self.model.timer_save = 0
                        self.frame.showPanel(self.frame.panelSave)
                    case EVENT.CANCEL | EVENT.TIMER_ALCO:
                        self.model.state = STATE.POST
                        self.model.timer_alco = 0
                        self.frame.showPanel(self.frame.panelPost)
                    case EVENT.TIMER:
                        self.model.timer_alco += 1
                        if self.model.is_timer_alco:
                            self.put_event(EVENT.TIMER_ALCO)
                    case EVENT.ERROR:
                            self.model.state = STATE.ERROR
                            self.model.timer_error = 0
                            self.frame.showPanel(self.frame.panelErro)


            case STATE.SAVE:
                match event:
                    case EVENT.TIMER:
                        self.model.timer_save += 1
                        if self.model.is_timer_save:
                            self.put_event(EVENT.TIMER_SAVE)
                    case EVENT.TIMER_SAVE:
                            self.model.state = STATE.POST
                            self.save_btn(1)
                            self.frame.showPanel(self.frame.panelPost)
                    case EVENT.BTN_YES:
                            self.model.state = STATE.POST
                            self.save_btn(1)
                            self.frame.showPanel(self.frame.panelPost)
                    case EVENT.BTN_NO:
                            self.model.state = STATE.POST
                            self.save_btn(0)
                            self.frame.showPanel(self.frame.panelPost)
                    case EVENT.ERROR:
                            self.model.state = STATE.ERROR
                            self.model.timer_error = 0
                            self.frame.showPanel(self.frame.panelErro)



    def save_pump_data(self):
        try:
            row_id = int(self.model.row_id)
            E = str(self.model.pump_data['E'])
            S = int(self.model.pump_data['S'])
            M = int(self.model.pump_data['M'])
            D = int(self.model.pump_data['D'])
            P = int(self.model.pump_data['P'])
            L = int(self.model.pump_data['L'])
            P_max = int(self.model.pump_data['max'])
            Move = int(self.model.pump_data['M'])
            T = int(self.model.pump_data['T'])
            piro = self.model.piro_data
            result, data, error_message = self.rest.save_data(row_id, E, S, M, D, P, L, P_max, Move, T, dissatisfied=1, Alc=0, Pir=piro)
            if result:
                self.model.mdata = data
            else:
                self._log.error(f'{error_message}')
                self.model.last_error_message = error_message
                self.show_post(EVENT.ERROR)

                

        except Exception as ex:
            raise Exception(f"Error on save_pump_data: {ex=}")

    def save_btn(self, btn=1):
        try:
            row_id = int(self.model.row_id)
            result, error_message = self.rest.save_btn(row_id, btn)
            if not result:
                self._log.error(f'{error_message}')
                self.model.last_error_message = error_message
                self.show_post(EVENT.ERROR)

        except Exception as ex:
            raise Exception(f"Error on save_btn: {ex=}")

        
        
        

    def run(self):
        while True:
            e = self.get_event()
            if e != EVENT.TIMER:
                self._log.info(f'{EVENTS[e]}') if e in EVENTS.keys() else self._log.error(f'EVENT.UNKNOWN:{e}')
            try:
                self.do_step(e)
            except Exception as ex:
                self._log.error(str(ex))
                self.put_event(EVENT.ERROR)

            if self._terminated:
                break
        self._log.info('stop run')
    
    def test(self):
        print(f'success, app_data is: {self._app_data}')
        self.state = 1
        pass

    def show_post(self):
        print("aafasdf")

    def on_card_data_is_ready(self, card):
        self._log.info(f'test callback, on_card_data_is_ready, card: {card}')
        self.model.card = card
        self.put_event(EVENT.CARD)

    def on_pump_data_is_ready(self, data):
        self._log.info(f'test callback, on_pump_data_is_ready, data:{data}')
        self.model.pump_data = data
        self.model.piro_data  = '-'
        self.model.alco_data = '---'
        self.put_event(EVENT.PUMP)

    def on_alco_data_is_ready(self, data):
        self._log.info(f'test callback, on_aclo_data_is_ready, data:{data}')
        self.put_event(EVENT.ACLO)

    def on_piro_data_is_ready(self, data):
        self._log.info(f'test callback, on_piro_data_is_ready, data:{data}')
        self.model.piro_data = str(data)
        self.put_event(EVENT.PIRO)

    def terminate(self):
        self._terminated = True

    def stop(self):
        self._terminated = True


    def get_event(self):
        try:
            event = self._queue.get(timeout=1)
        except queue.Empty:
            event = EVENT.TIMER
        return event

    def put_event(self, event):
        self._queue.put(event)

def test():
    print('test A')
    logg = log.Log().getLogger(name='test')
    logg.info('start test')
    _args = Args()

    automat = Automat(logg, _args)
    automat.start()
    n = 4
    for i in range(n):
        time.sleep(1)
        logg.info(f'put event {i}...')
        automat.put_event(i)
    automat.stop()
    # automat.join()
   

if __name__ == "__main__":
    test()
