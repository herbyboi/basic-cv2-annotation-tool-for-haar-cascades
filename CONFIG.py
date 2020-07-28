import glob
import os


class CONFIG():
    fl = 'config.cnf'

    @classmethod
    def fetch(cls,req):
        with open(cls.fl,'r') as cnf:
            sttcnf = cnf.readlines()
        for ln in sttcnf:
            if ln.startswith(f'|{req}'):
                args = ln.split("//")[1:]
                ret = []
                for el in args:
                    nEl = el.replace(' ','').replace('\n','')
                    ret.append(nEl)
                return ret

    @classmethod
    def isInside(cls,x,y,obj):
        xb,yb,wb,hb = obj
        if x > xb and x < xb + wb and y > yb and y < yb + hb:
            return True

        return False

    @classmethod
    def prettyfy(cls,lst):
        placeholder = ''
        for el in lst:
            placeholder += f'{el} '

        return placeholder

    @classmethod
    def getfreename(cls, dir, prefix):
        num = len(glob.glob(f'{dir}\\{prefix}*.txt'))
        if num != 0:
            return num
        return ''

    @classmethod
    def readOld(cls,path):
        with open(path,'r') as fl:
            data = fl.readlines()
            sets = []
            for el in data:
                set = [el.split(' ')]
                sets.append(set)
        return sets

    @classmethod
    def splitbyfour(cls,lst):
        lst = lst[:-1]
        bitz = []
        crit = 4
        cnt = 1
        bit = []
        for el in lst:
            bit.append(int(el))
            if cnt == 4:
                cnt = 1
                bitz.append(bit)
                bit = []
            cnt += 1
        print(bitz)
        return bitz









