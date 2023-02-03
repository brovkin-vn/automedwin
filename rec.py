from unittest import result
import face_recognition
import cv2
import numpy as np
import base64

from log import Log
from args import Args
from cam import Cam
from rest import Rest

class Rec():

    def __init__(self, log, args, cam, rest):
        super().__init__()
        self._log: Log = log
        self._args: Args = args
        self._cam: Cam = cam
        self._rest: Rest = rest
        self._face_actual = ''
        self._complete = None
        self._flag = None
        self._log.info(f'init face recognition module')

    def reset_face_recognition(self):
        self._complete = False

    # def readb64(self, uri):
    #     encoded_data = uri.split(',')[1]
    #     nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    #     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #     return img
    
    def start_face_recognition(self, rowid):
        if self._args.disable_recognition: return
        if not self.complete: # 
            result, img = self._cam.get_face()
            if result:
                face_code = face_recognition.face_encodings(img[:, :, ::-1]) 
                result = len(face_code) > 0 and len(face_code[0]) == 128
                print(f'{len(face_code[0])=}')
                if result:
                    result, img_sample = self._rest.get_face_sample_by_rowid(rowid)
                    if result:
                        face_code_sample = face_recognition.face_encodings(img_sample[:, :, ::-1]) 
                        result = len(face_code_sample) > 0 and len(face_code_sample[0]) == 128
                        print(f'{len(face_code_sample[0])=}')
                        if result:
                            matches = face_recognition.compare_faces([face_code_sample[0]], face_code[0])
                            if len(matches) > 0:
                                self._complete = True
                                self._flag = True in matches
                                face_locations = face_recognition.face_locations(img[:, :, ::-1])
                                self._log.debug(f'{len(face_locations)=}')
                                if (len(face_locations) > 0):
                                    fl = face_locations[0]
                                    top, right, bottom, left = fl[0], fl[1], fl[2], fl[3]
                                    self._log.debug(f'{top=}, {bottom=}, {left=}, {right=}')
                                    self._face_actual = img[top:bottom, left:right]
                        else:
                            self._log.error(f'no face to encoding on sample image')        
                    else:
                        self._log.error(f'no face sample image')        
                else:
                    self._log.debug(f'no face to encoding')
            else:
                self._log.error(f'no face image')
        
        

            



    @property
    def complete(self):
        return self._complete

    @property
    def flag(self):
        return self._flag

    @property
    def face_actual(self):
        return self._face_actual


def test():
    print('test recognition')
    _args = Args()
    _log = Log().getLogger(name='test')
    _cam = Cam(log=_log)
    _rest = Rest(log=_log)

    rec = Rec(log=_log, args=_args, cam=_cam, rest=_rest)
    rec.reset_face_recognition()
    rec.start_face_recognition(rowid=113)

    print(f'{rec.complete=}, {rec.flag=}')
    if rec.complete:
        cv2.imshow("img", rec.face_actual)       
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
    
if __name__ == "__main__":
    test()
