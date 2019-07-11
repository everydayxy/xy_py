#coding=utf8

import time
import datetime
from dateutil.relativedelta import relativedelta

class TimeOperation:

    def strtodate(self, tstr1, fmt):
        try:
            return datetime.datetime.strptime(tstr1, fmt)
        except:
            return None

    def datetostr(self, t, fmt):
        try:
            return datetime.datetime.strftime(t, fmt)
        except:
            return None

    def getperiod(self, tstr1, tstr2, fmt, rfmt):
        result = []
        try:
            t1 = datetime.datetime.strptime(tstr1, fmt)
            t2 = datetime.datetime.strptime(tstr2, fmt)
            tdelta = relativedelta(days=1)

            while t1 <= t2:
                if rfmt == None:
                    result.append(t1)
                else:
                    result.append(t1.strftime(rfmt))
                t1 += tdelta
        except:
            pass
        return result


class DataOperation:

    def read_data_file(self, fname, separator, cidx):
        '''This function read fname, get all columns specified by *cidx

            fname: str
            cidx: list of integers
            separator: the character which separates columns
        '''
        result = []
        try:
            f = open(fname)
        except:
            return result
        line = f.readline().strip()
        while line != '':
            parts = line.split(separator)
            result.append([parts[idx].strip() for idx in cidx])
            line = f.readline().strip()
        f.close()
        return result