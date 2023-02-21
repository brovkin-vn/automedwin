#coding: utf-8
from encodings import utf_8
from subprocess import Popen, PIPE
import sys
import urllib3
import urllib
import xml.etree.ElementTree as etree
import serial.tools.list_ports



def list_ports():
    print(sys._getframe().f_code.co_name)
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
    for port in sorted(ports):
        print(f"{port}")

def alco():
    try:
        desc_mask = "cp210x"
        desc_mask = "LOCATION=1-1.1.1"
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if desc_mask in  hwid:
                return True, port
        return False, 'None'
    except:
        return False, 'None'

def piro():
    try:
        desc_mask = "CH340"
        desc_mask = "LOCATION=1-1.2.3"
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if desc_mask in  hwid:
                return True, port
        return False, 'None'
    except:
        return False, 'None'

def addr():
    try:
        command = 'route PRINT|find " 0.0.0.0"'
        s = Popen(command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().decode()
        ip = " ".join(s.split()).split(' ')[3]
        # print(f"{ip=}")
        return '10.' in ip, ip
    except:
        return False, 'None'

def router1():
    try:
        command = 'route PRINT|find " 0.0.0.0"'
        s = Popen(command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().decode()
        gateway = " ".join(s.split()).split(' ')[2]
        # print(f"{gateway=}")
        return '10.' in gateway, gateway
    except:
        return False, 'None'


def router2():
    try:
        command = 'ping -n 1 pnoc-server9.uku.evraz.com|find "TTL"'
        # print(command)
        s = Popen(command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().decode("IBM866")
        # print(f"command result: {len(s)=}: {s=}")
        return len(s) > 0, s
    except Exception as e:
        print(e)
        return False, 'None'

def server1():
    try:
        http = urllib3.PoolManager()
        url = f"http://pnoc-server9.uku.evraz.com:8089/video/test-server-medic.php"
        resp = http.request('GET', url)
        
        if resp.status == 200:
            data = resp.data.decode('utf8')
            return 'ok' in data, resp.reason
        else:
            return False, 'None'
    except Exception as e:
        print(e)
        return False, 'None'

def server2():
    try:
        http = urllib3.PoolManager()
        url = f"http://hq-server62/AxisWebApp/services/CardlibIntegrationService2Port?wsdl"
        resp = http.request('GET', url)
        if resp.status == 200:
            root = etree.fromstring(resp.data.decode('utf8'))
            return root[0][0][0].attrib['name'] == 'getCards', resp.reason
        else:
            return False, 'None'

    except Exception as e:
        print(e)
        return False

def test():
    list_ports()   
    print(f"start check")
    print(f"check alco: {alco()}")
    print(f"check piro: {piro()}")
    print(f"check addr: {addr()}")
    print(f"check router1: {router1()}")
    print(f"check router2: {router2()}")
    print(f"check server1: {server1()}")
    print(f"check server2: {server2()}")



if __name__ == '__main__':
    test()
