# Программа медицинских осмотров

### запуск
usage: automed.exe [-h] [-ev] [-dr] [-ea] [-ep] [-pump PUMP_PORT]
                   [-alco ALCO_PORT] [-piro PIRO_PORT] [-id MODULE_ID]

Аргументы приложения АС Медосмотры

options:
  -h, --help            show this help message and exit
  -ev, --enable_verbose
                        Включить расширенное журналирование
  -dr, --disable_recognition
                        Отключить распознование лица
  -ea, --enable_alco    Включить функцию алкотестирвания
  -ep, --enable_piro    Включить функцию замера температуры
  -pump PUMP_PORT       Порт тономертра, по умочанию COM1
  -alco ALCO_PORT       Порт алкотестера, по умочанию COM3
  -piro PIRO_PORT       Порт пирометра, по умочанию COM4
  -id MODULE_ID         Номер модуля, по умочанию 99

### запустить программу с номером модуля 162, включить функцию замера температуры
automed -id=162 -ep
