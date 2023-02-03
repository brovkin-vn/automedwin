import argparse

class Args(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Args, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Аргрументы приложения АС Медосмотры')
        self.parser.add_argument('-ev', '--enable_verbose', action='store_true', help="Включить расширенное журналирование")
        self.parser.add_argument('-dr', '--disable_recognition', action='store_true', help="Отключить распознование лица")
        self.parser.add_argument('-ea', '--enable_alco', action='store_true', help="Включить функцию алкотестирвания")
        self.parser.add_argument('-ep', '--enable_piro', action='store_true', help="Включить функцию замера температуры")
        self.parser.add_argument('-pump', dest="pump_port", default='COM1', type=str, help='Порт тономертра, по умочанию COM1')
        self.parser.add_argument('-alco', dest="alco_port", default='COM2', type=str, help='Порт алкотестера, по умочанию COM2')
        self.parser.add_argument('-piro', dest="piro_port", default='COM3', type=str, help='Порт пирометра, по умочанию COM3')
        self._args = self.parser.parse_args()
        # print(arguments)


    @property
    def args(self):
        return self._args
        # return self.parser.parse_args()
    @property
    def enable_verbose(self):
        return self._args.enable_verbose

    @property
    def disable_recognition(self):
        return self._args.disable_recognition

    @property
    def enable_alco(self):
        return self._args.enable_alco

    @property
    def enable_piro(self):
        return self._args.enable_piro

    @property
    def pump_port(self):
        return self._args.pump_port

    @property
    def alco_port(self):
        return self._args.alco_port

    @property
    def piro_port(self):
        return self._args.piro_port

def test():
    args = Args()
    print(f'{args.args=}')
    print(f'{args.enable_verbose=}')
    print(f'{args.disable_recognition=}')
    print(f'{args.enable_alco=}')
    print(f'{args.enable_piro=}')
    print(f'{args.pump_port=}')

if __name__ == '__main__':
    test()

