'''
@author:lcl
@email:liquidio@qq.com
文档：https://pypi.org/project/kociemba/
# 输入表示：
             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|
             
输入排列顺序U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2, R3, R4, R5, R6, R7, R8, R9, F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9, L1, L2, L3, L4, L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9.


# 输出表示：
1. 单个字母表示那个面顺时针旋转90度
2. 单个字母后有单引号表示那个面逆时针旋转90度
3. 单个字母后有个数字2表示那个面旋转180度
例子R U R’ U R U2 R’ U

# 颜色表示
U代表U面的颜色，F代表F面的颜色。。。  
U面中心点为U颜色。
# 通信
@todo: 通讯协议尚未确定
一个步骤发送一次命令知道返回完成，才继续发送下一个步骤
'''
import sys
import json
import serial
from serial.tools.list_ports import comports
from cv2 import cv2

from detection import Sole,Cube

#串口通信波特率
BPS = 115200
#超时时间
TIMEX = 1
svm = cv2.SVM()
#@todo初步确定参数
svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                svm_type = cv2.SVM_C_SVC,
                C=2.67, gamma=5.383 )

def print_serial():
    port_list = list(comports())
    for port in port_list:
            print(port)

def serial_init(port='COM1'):
    try:
        return serial.Serial(port,BPS,timeout=TIMEX)
    except:
        return None

def training():
    with open ('svm_date.json','r') as f:
        svm_date = json.loads(f.read())
    with open ('svm_label.json','r') as f:
        svm_label = json.loads(f.read())
    svm.train(svm_date,svm_label, params=svm_params)
    svm.save('core.xml')

def solver():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
            print("can't open video")
            sys.exit()
    svm.loads('core.xml')
    cube = Cube()
    color_list = cube.get()
    result = svm.predict_all(color_list)
    cube.roate(result)
    print('finish!')

if __name__ == '__main__':
    solver()