from cv2 import cv2
import numpy as np
import json
import serial
from serial.tools.list_ports import comports

class Sole:
        def __init__(self,frame):
                self.frame = frame
                self.svm = []
        def pre_dispose(self):#返回一个面上的颜色平均值HSVRGB
                img = cv2.GaussianBlur(self.frame,(7,7),0)
                b,g,r = cv2.split(img)
                avgb = cv2.mean(b)[0]
                avgg = cv2.mean(g)[0]
                avgr = cv2.mean(r)[0]
                k = (avgb+avgg+avgr)/3
                kb = k/avgb
                kg = k/avgg
                kr = k/avgr
                b = cv2.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)
                g = cv2.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
                r = cv2.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
                img = cv2.merge([b,g,r])
                img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                h,s,v = cv2.split(img_hsv)
                v = cv2.equalizeHist(v)
                img_hsv =  cv2.merge([h,s,v])
                self.img_hsv = img_hsv
                img =  cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
                self.img_bgr = img
        def get_img(self):
                return self.img_bgr
        def get_svm_date(self):
                '''
                #HSVRGB 平均值
                '''
                bgr = np.mean(self.img_bgr)
                hsv = np.mean(self.img_hsv)
                return (bgr+hsv)/2
        def set_roi(self,x,x1,y,y1):
                self.frame = self.frame[x:x1,y:y1]
                cv2.imwrite("roi.array",[x,x1,y,y1])
        def get_roi(self):
                return cv2.imread('roi.array')
        def set_svm_label(self,label):
                if(type(label) is np.array):
                        self.svm_label = label
                        return True
                return False
        def set_svm(self,data,label):
                self.svm.append([data,label])
                with open('svm_date','w') as f:
                        f.write()
        def get_svm(self):
                json =''
                with open('svm_date','r') as f:
                        json = f.read()
                return json.dump()
        #svm 训练
        def training(self):
                svm = cv2.ml.SVM_create() #创建SVM model 
                data = cv2.imread('svm_data.array')
                label = cv2.imread('svm_label.array')
                #属性设置
                svm.setType(cv2.ml.SVM_C_SVC)
                svm.setKernel(cv2.ml.SVM_LINEAR)#线性核
                svm.setC(0.01)
                #训练
                self.svm_sole = svm.train(data,cv2.ml.ROW_SAMPLE,label)
                svm.save('core.array')
        def get_svm_sole(self):
                return cv2.imread('core.array')

class Cube(Sole):
        def __init__(self):
                self.u_face =0
                self.d_face =0
                self.l_face =0
                self.r_face =0
                self.f_face =0
                self.b_face =0
        def serial_init(self,port):
                port_list = list(comports())
                for port in port_list:
                        print(port)
                bps = 115200
                timex = 5
                self.serial = serial.Serial(port,bps,timeout=timex)
        def roate(self,command):
                if (type(command) is str)and (len(command)>0):
                        self.serial.write('#'+command+'#')
                        while True:
                                r = self.serial.read()
                                if r == command+'ok':
                                        return True
                                else:
                                        return False
        def get_code(self):
                pass

import sys
if __name__ == "__main__":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
                print("can't open video")
                sys.exit()
        while True:
                ret,frame = cap.read()
                video = Sole(frame)
                cv2.imshow('img',video.get_img())
                print("svm date:",video.get_svm_date())
                if cv2.waitKey(1)&0xff == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()