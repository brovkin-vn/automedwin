from unittest import result
from numpy import full
import urllib3
# import logging
import yaml
import xml.etree.ElementTree as etree
import cv2
import numpy as np
import base64
from log import Log



class Rest():


    def __init__(self, log) -> None:

        self._log:Log = log
        self._log.info(f'init rest module')
        pass



    def save_btn(self, id=5607678,btn=1):

        result = False
        error_message = ''
        data = {}

        try: 
            http = urllib3.PoolManager()
            url = f"https://pnoc-pc177.uku.evraz.com/medic/SaveBtnYaml.php?{id=}&{btn=}"
            self._log.info(f"{url=}")
            resp = http.request('GET', url)
            
            result = (resp.status == 200)
            
            if result:
                try:
                    # print(resp.data.decode('utf8'))
                    data=yaml.load(resp.data.decode('utf8'), Loader=yaml.loader.BaseLoader)
                    # print(f"{data=}")
                    result = (data['result'] == "OK")
                    # print(f"{result=}")
                    if not result: error_message = data['message']
                    # print(f"{error_message=}")

                    # full_name = d['fullName']
                    # row_id = d['rowId']
                except yaml.YAMLError as e:
                    self._log.error(e)
                    error_message = e
                    


        except Exception as e:
            self._log.error(e)
            error_message = e

        return result, error_message



    def save_data(self, id=5524706,E=0,S=120,M=10,D=80,P=0,L=0,P_max=0,Move=0,T=0,dissatisfied=0,Alc=0,Pir=0):

        result = False
        full_name = 'none'
        error_message = ''
        row_id = -1
        data = {}

        try: 
            print('111111')
            http = urllib3.PoolManager()
            url = f"https://pnoc-pc177.uku.evraz.com/medic/SaveMedicYaml.php?{id=}&E={E}&{S=}&{M=}&{D=}&{P=}&{L=}&{P_max=}&{Move=}&{T=}&{dissatisfied=}&{Alc=}&Pir={Pir}"
            print('111112')
            self._log.info(f"{url=}")
            resp = http.request('GET', url)
            print('111113')
            result = (resp.status == 200)
            full_name = 'none'
            row_id = -1
            print('111114')
            if result:
                try:
                    # print(resp.data.decode('utf8'))
                    print('  111111')
                    data=yaml.load(resp.data.decode('utf8'), Loader=yaml.loader.BaseLoader)
                    print('  111112')
                    print(data)
                    print('  111113')
                    result = (data['result'] == "OK")
                    print('  111114')
                    # full_name = d['fullName']
                    # row_id = d['rowId']
                except yaml.YAMLError as e:
                    self._log.error(e)
                    error_message = e
                    


        except Exception as e:
            self._log.error(e)
            error_message = e

        return result, data, error_message


    def get_full_name_by_card(self, card=27566568, box_id=99):

        result = False
        full_name = 'none'
        error_message = ''
        row_id = -1

        try: 
            card1 = (card >> 1) & 0xFFFF
            card2 = (card >> 17) & 0xFF
            http = urllib3.PoolManager()
            url = f"https://pnoc-pc177.uku.evraz.com/medic/indexYaml.php?card1={card1}&card2={card2}&id={box_id}"

            resp = http.request('GET', url)
            
            result = (resp.status == 200)
            full_name = 'none'
            row_id = -1
            
            if result:
                try:
                    d=yaml.load(resp.data.decode('utf8'), Loader=yaml.loader.BaseLoader)
                    result = (d['result'] == "OK")
                    full_name = d['fullName']
                    row_id = d['rowId']
                except yaml.YAMLError as e:
                    self._log.error(e)
                    error_message = e
                    


        except Exception as e:
            self._log.error(e)
            error_message = e

        return result, full_name, row_id, error_message


    def get_face_sample_by_rowid(self, rowid):   
        http = urllib3.PoolManager()
        url = f'https://pnoc-server9.uku.evraz.com/medic/GetPhoto.php?id={rowid}'
        resp = http.request('GET', url)
        result = (resp.status == 200)

        if result:
            try:
                tree = etree.fromstring(resp.data.decode())
                src_data =  tree.attrib['src']
                encoded_data = src_data.split(',')[1]
                nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                result = False
                self._log.error(e)
        return result, img

    def test(self):
        self.save_data()
        # _, full_name, row_id =  self.get_full_name_by_card(card1=20724, card2=210, box_id=99, card_full=-1)
        # print(f'Test is:{_}, full_name: {full_name}, row_id = {row_id}')
        
        # rowid = 113 
        # result, img = self.get_face_sample_by_rowid(rowid)
        # print(f'get_uri {result=}')
        # if result:
        #     cv2.imshow("face sample by rowid 113", img)       
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()



if __name__ == "__main__":
    _log = Log().getLogger(name='test')
    rest = Rest(log=_log)
    rest.test()

