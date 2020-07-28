import glob
import re
import os
import cv2
import numpy as np
from CONFIG import CONFIG

class Image():
    DIR = CONFIG.fetch(r"dir")[0]
    formats = CONFIG.fetch(r'formats')
    chunks = []
    lowerBorder = int(CONFIG.fetch('Lborder')[0])
    OutDir = CONFIG.fetch(r"outdir")[0]
    prefix = CONFIG.fetch(r"prefix")[0]
    try:
        old = CONFIG.fetch('old_data')[0]
    except: old = False


    def __init__(self):
        self.images = []
        for format in self.formats:
            for fl in glob.glob(f'{self.DIR}\\*.{format}'):
                self.images.append(fl)

        self.images.sort()
        self.workonid = self.images[0]

        self.objDict = {}
        for fl in self.images:
            self.objDict[fl] = []

        if self.old:
            data = CONFIG.readOld(self.old)
            for el in data:
                bitz = CONFIG.splitbyfour(el[0][2:])

                for bit in bitz:
                    II = []
                    for I in bit:
                        II.append(int(I))
                    print(II)
                    self.objDict[el[0][0]].append(II)


        cv2.imshow('tool_1',self.grabImg())
        cv2.setMouseCallback('tool_1',self.onmouse)


    def grabImg(self):
        canvas = cv2.imread(self.workonid)
        for obj in self.objDict[self.workonid]:
            x,y,w,h = obj
            if w < self.lowerBorder or h < self.lowerBorder:
                cv2.rectangle(canvas,(x,y),(x+w,y+h),(0,0,255),4)
            else:
                cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 255, 0),4)
        return canvas.copy()

    def nextImage(self):
        cur = self.images.index(self.workonid)
        if cur + 1 > len(self.images) - 1:
            self.workonid = self.images[0]
        else:
            self.workonid = self.images[cur + 1]

    def prevImage(self):
        print('called')
        cur = self.images.index(self.workonid)
        if cur - 1 < 0:
            self.workonid = self.images[len(self.images) - 1]
        else:
            self.workonid = self.images[cur - 1]
        print(self.workonid)


    def grabRoi(self):
        roi = cv2.selectROI('tool_1',self.grabImg(),True)
        cv2.setMouseCallback('tool_1',self.onmouse)
        x,y,w,h = roi
        self.objDict[self.workonid].append([x,y,w,h])

    def onmouse(self, k, x, y, s, p):
        if k == cv2.EVENT_LBUTTONDBLCLK:
            print(x,y)
            self.rm((x,y))

    def rm(self, tup):
        x,y = tup
        for obj in self.objDict[self.workonid]:
            print(CONFIG.isInside(x,y,obj))
            if CONFIG.isInside(x,y,obj):
                print(self.objDict[self.workonid].index(obj))
                self.objDict[self.workonid].pop(self.objDict[self.workonid].index(obj))


    def writeUp(self):
        with open(f'{self.OutDir}\\{self.prefix}{CONFIG.getfreename(self.OutDir,self.prefix)}.txt','a') as fl:
            for k,v in self.objDict.items():
                print(len(v))
                if len(v) > 0:
                    line = np.concatenate(v.copy())
                    print(f'{k} {int(len(line)/4)} {CONFIG.prettyfy(line)}',file=fl)


    def run(self):
        while 1:
            try:
                cv2.imshow('tool_1',self.grabImg())







                key = cv2.waitKey(1)
                if key == 27:
                    self.writeUp()
                    break

                if key == ord('q'):
                    self.nextImage()

                if key == ord('e'):
                    self.prevImage()

                if key == ord('w'):
                    self.grabRoi()

                if key == ord('s'):
                    self.writeUp()

            except Exception as e:
                with open(f'{self.OutDir}\\logz.txt','a') as logz:
                    print(f'exception boiz, its-a {e} \n')
                    quit()










im = Image()
im.run()


