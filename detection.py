from cv2 import cv2
import numpy as np
import json
import sys
from solver import serial_init

class Sole:
        def __init__(self,frame):
                self.frame = frame
        def run(self):
                self.pre_dispose()
                self.get_roi()
                self.get_svm_date()
                self.save()
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
                self.frame = img
        def get_visual(self):
                self.pre_dispose()
                return self.img_bgr
        def get_svm_date(self):
                '''
                #HSVRGB 平均值
                '''
                y,y1,x,x1 = self.roi
                self.svm_date = []
                height = (x1-x)/3
                width = (y1-y)/3
                #图像分为9个区域，计算9个区域的hsv 和 bgr 的平均值，返回数组self.svm
                for i in range(3):
                        for j in range(3):
                                t = self.img_bgr[(y+i*height):(y+height*(i+1)),(x+j*width):(x+width(j+1))]
                                t1 = self.img_hsv[(y+i*height):(y+height*(i+1)),(x+j*width):(x+width(j+1))]
                                bgr = np.mean(t)
                                hsv = np.mean(t1)
                                self.svm_date.append((bgr+hsv)/2)
                return self.svm_date
        def get_roi(self):
                with open ("roi.json",'r') as f:
                        roi = f.read()
                        roi = json.loads(roi)
                        self.frame = self.frame[roi[0]:roi[1],roi[2]:roi[3]]
                        self.roi = roi
                        return roi
        def roi_init(self):
                with open('roi.json','w') as f:
                        f.write(json.dumps(range(4)))
        def save(self):
                with open ('svm_date.json','r') as f:
                        pre = f.read()
                        pre = json.loads(pre)
                with open ('svm_date.json','w') as f:
                        now = pre + self.svm_date
                        f.write(json.dumps(now))

def load():
        with open ('svm_date.json','r') as f:
                return json.loads(f.read())

class Cube:
        def __init__(self,port='COM1'):
                self.cap_command = ''
                self.face = []
                self.serial = serial_init(port)
                self.svm_date_init()
                self.video = cv2.VideoCapture(0)
                if not cap.isOpened():
                        print("can't open video")
                        sys.exit()
        def __del__(self):
                self.serial.close()
        def cap(self):
                ret,frame = self.video.read()
                return frame
        def sort_face(self):
                #@todo:如何调换面的顺序
                pass
        def svm_date_init(self):
                with open ('svm_date.json','w') as f:
                        f.write(json.dumps([1]))
        def roate(self,command):
                if (type(command) is str)and (len(command)>0):
                        self.is_busy = True
                        self.serial.write('@'+command+'\n')
                        while True:
                                r = self.serial.readline()
                                if r == command:
                                        self.is_busy = False
                                        return True
        def get(self):
                for i in self.cap_command :
                        if not self.is_busy:
                                self.roate(i)
                                self.face.append(self.cap())
                self.sort_face()
                for i in self.face:
                        Sole(i).run()
                return load()
##测试
if __name__ == "__main__":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
                print("can't open video")
                sys.exit()
        while True:
                ret,frame = cap.read()
                video = Sole(frame) 
                print(video.get_roi())
                cv2.imshow('img',video.get_visual())
                if cv2.waitKey(1)&0xff == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()