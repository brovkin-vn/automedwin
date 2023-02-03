TIMER_PUMP_SETPOINT = 120
TIMER_PIRO_SETPOINT = 30
TIMER_ALCO_SETPOINT = 30
TIMER_ERROR_SETPOINT = 3
TIMER_TEST_SETPOINT = 20
TIMER_SAVE_SETPOINT = 20

class EVENT:
    ERROR       = -1
    START       = 0
    CARD        = 1
    PUMP        = 2
    TEST        = 3
    CANCEL      = 4
    TIMER       = 5
    TIMER_PUMP  = 6
    TIMER_ERROR = 7
    TIMER_TEST  = 8
    BTN_YES     = 9
    BTN_NO      = 10
    TIMER_SAVE  = 11
    TIMER_PIRO  = 12
    TIMER_ALCO  = 13
    PIRO        = 14
    ALCO        = 15


EVENTS = {
    EVENT.ERROR:       "EVENT.ERROR",
    EVENT.START:       "EVENT.START",
    EVENT.CARD:        "EVENT.CARD",
    EVENT.PUMP:        "EVENT.PUMP",
    EVENT.TEST:        "EVENT.TEST",
    EVENT.CANCEL:      "EVENT.CANCEL",
    EVENT.TIMER:       "EVENT.TIMER",
    EVENT.TIMER_PUMP:  "EVENT.TIMER_PUMP",
    EVENT.TIMER_ERROR: "EVENT.TIMER_ERROR",
    EVENT.TIMER_TEST:  "EVENT.TIMER_TEST",
    EVENT.BTN_YES:     "EVENT.BTN_YES",
    EVENT.BTN_NO:      "EVENT.BTN_NO",
    EVENT.TIMER_SAVE:  "EVENT.TIMER_SAVE",
    EVENT.TIMER_PIRO:  "EVENT.TIMER_PIRO",
    EVENT.TIMER_ALCO:  "EVENT.TIMER_ALCO",
    EVENT.PIRO:        "EVENT.PIRO",
    EVENT.ALCO:        "EVENT.ALCO"
    }

class STATE:
    ERROR = -1
    START = 0
    POST  = 1
    PUMP  = 2
    SAVE  = 3
    PIRO  = 4
    ALCO  = 6
    TEST  = 7
    QUERY = 8

STATES = {
    STATE.ERROR: "STATE.ERROR",
    STATE.START: "STATE.START",
    STATE.POST:  "STATE.POST",
    STATE.PUMP:  "STATE.PUMP",
    STATE.SAVE:  "STATE.SAVE",
    STATE.PIRO:  "STATE.PIRO",
    STATE.ALCO:  "STATE.ALCO",
    STATE.TEST:  "STATE.TEST",
    STATE.QUERY: "STATE.QUERY"
    }

class Model():

    def __init__(self, log) -> None:
        print(f"INIT MODEL INIT MODEL INIT MODEL INIT MODEL INIT MODEL INIT MODEL INIT MODEL INIT MODEL INIT MODEL ")
        self.log = log

        self._app_data = '2022-09-12'
        self._app_version = '0.000'
        self._app_name = 'automed'
        self._state = STATE.START
        self._card:int = 0
        self._box_id = 99
        self._timer_pump = 0
        self._timer_error = 0
        self._timer_test = 0
        self._timer_save = 0
        self._timer_piro = 0
        self._timer_alco = 0
        self._last_error_message = ''
        self._full_name =  ''
        self._row_id = -1
        self._piro_data:str = '-'
        self._aclo_data:str = '-'
        self._pump_data = {"T":"00:00", "S":"-", "D":"-", "P":"-", "A":"-"}


        self.log.info(
            f'init model, {self._app_name=}, {self._app_version=}, {self._app_data=}')
        pass

    def clear_card_data(self):
        self._full_name = ''
        self.last_error_message = ''
        self._row_id = -1

    def set_card_data(self, result):
        self._full_name = result[1]
        self._row_id = result[2]
        self._last_error_message = result[3]


    @property
    def piro_data(self):
        return str(self._piro_data)

    @piro_data.setter
    def piro_data(self, value):
        self._piro_data = str(value)

    @property
    def alco_data(self):
        return self._alco_data

    @alco_data.setter
    def alco_data(self, value):
        self._alco_data =value

    @property
    def pump_data(self):
        return self._pump_data

    @pump_data.setter
    def pump_data(self, value):
        self._pump_data =value

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def full_name(self, value):
        self._row_id =value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name =value

    @property
    def last_error_message(self):
        return self._last_error_message

    @last_error_message.setter
    def last_error_message(self, value):
        print(f"last_error_message.setter: = {str(value)=}")
        self._last_error_message = str(value)

    @property 
    def box_id(self):
        return self._box_id

    @property 
    def timer_test(self):
        return self._timer_test

    @property 
    def is_timer_test(self):
        return self._timer_test > TIMER_TEST_SETPOINT

    @timer_test.setter
    def timer_test(self, value):
        self._timer_test = value

    @property 
    def timer_pump(self):
        return self._timer_pump

    @property 
    def is_timer_pump(self):
        return self._timer_pump > TIMER_PUMP_SETPOINT

    @timer_pump.setter
    def timer_pump(self, value):
        self._timer_pump = value

    @property 
    def timer_error(self):
        return self._timer_error

    @property 
    def is_timer_error(self):
        return self._timer_error > TIMER_ERROR_SETPOINT

    @timer_error.setter
    def timer_error(self, value):
        self._timer_error = value

    @property 
    def timer_save(self):
        return self._timer_save

    @property 
    def is_timer_save(self):
        return self._timer_save > TIMER_SAVE_SETPOINT

    @timer_save.setter
    def timer_save(self, value):
        self._timer_save = value

    @property 
    def timer_piro(self):
        return self._timer_piro

    @property 
    def is_timer_piro(self):
        return self._timer_piro > TIMER_PIRO_SETPOINT

    @timer_piro.setter
    def timer_piro(self, value):
        self._timer_piro = value

    @property 
    def timer_alco(self):
        return self._timer_alco

    @property 
    def is_timer_alco(self):
        return self._timer_alco > TIMER_ALCO_SETPOINT

    @timer_alco.setter
    def timer_alco(self, value):
        self._timer_alco = value

    @property
    def app_data(self):
        return self._app_data

    @property
    def app_version(self):
        return self._app_version

    @property
    def app_name(self):
        return self._app_name

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value):
        if type(value) == int:
            self._card = value
        else:
            try:
                self._card = int(value, 16)
            except Exception as e:
                self.log.error(f"error on decode {value=}, {e}")
                self.last_error_message = e



    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            self.log.info(
                f'change model state from {STATES[self._state]} to {STATES[value]}')

        self._state = value

    def test(self):
        print(f'success, app_data is: {self._app_data}')
        self.state = 1
        pass


if __name__ == "__main__":
    rest = Model()
    rest.test()
