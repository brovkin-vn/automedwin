from unittest import result
import cv2
import base64
import numpy as np
 
from log import Log

class Cam():

    def __init__(self, log):
        super().__init__()
        self._log:Log = log
        self._log.info(f'init camera module')
        


    def img2base64(self, img):
        ret, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer)

    def base64_2img(self, uri):
        # encoded_data = uri.split(',')[1]
        encoded_data = uri
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def get_face(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
        # cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        ret, frame = cap.read()
        # frame = cv2.imread("./test_img/brovkin.jpg")
        # frame = cv2.imread("./test_img/yurichev.png")
        
        # print(f'{type(frame)}')
        # cap.release()
        # rgb_frame = frame[:, :, ::-1]
        return ret, frame

def test():
    print('test camera')
    _log = Log().getLogger(name='test')
    cam = Cam(log=_log)

    try:
        r, img = cam.get_face()
        if r:
            cv2.imshow("img", img)       
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except Exception as e:
        print(f'error: {e}')

    
if __name__ == "__main__":
    test()
