usage: automed.exe [-h] [-ev] [-dr] [-ea] [-ep] [-pump PUMP_PORT]
                   [-alco ALCO_PORT] [-piro PIRO_PORT] [-id MODULE_ID]

��������� ���������� �� ����������

options:
  -h, --help            show this help message and exit
  -ev, --enable_verbose
                        �������� ����������� ��������������
  -dr, --disable_recognition
                        ��������� ������������� ����
  -ea, --enable_alco    �������� ������� ���������������
  -ep, --enable_piro    �������� ������� ������ �����������
  -pump PUMP_PORT       ���� ����������, �� �������� COM1
  -alco ALCO_PORT       ���� �����������, �� �������� COM3
  -piro PIRO_PORT       ���� ���������, �� �������� COM4
  -id MODULE_ID         ����� ������, �� �������� 99

# ��������� ��������� � ������� ������ 162, �������� ������� ������ �����������
automed -id=162 -ep