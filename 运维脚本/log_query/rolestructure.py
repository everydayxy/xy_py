#coding=utf8

import datetime

class Role:

    MAXLENGTH = 64

    def __init__(self, name, nflag=MAXLENGTH):
        self.name = name
        self.monthActiveFlag = 0
        self.monthActiveTime = [0]*(self.MAXLENGTH)
        self.monthRank = [1]*(self.MAXLENGTH)
        self.todayLoginCount = 0
        self.todayLogoutTime = []
        self.newCreateFlag = nflag
        self.isconsumer = -1
        self.money = [0]*(self.MAXLENGTH)

    def add_day(self, days=1):
        self.monthActiveFlag <<= days
        self.monthActiveFlag &= (1<<self.MAXLENGTH)-1
        del self.monthActiveTime[0:days]
        self.monthActiveTime += [0] * days
        self.monthActiveTime[-days] = self.get_today_online_time()
        del self.monthRank[0:days]
        self.monthRank += [0] * days
        if self.isconsumer >= 0: self.isconsumer += days
        del self.money[0:days]
        self.money += [0] * days
        self.todayLoginCount = 0
        self.todayLogoutTime = []
        if self.newCreateFlag < self.MAXLENGTH:
            self.newCreateFlag += days

    def mark_active(self, mask=1):
        self.monthActiveFlag |= mask

    def get_active(self, mask):
        return self.monthActiveFlag & mask

    def get_active_days(self, func):
        return func(self.monthActiveFlag)

    def get_today_online_time(self, idx=-1):
        delta = 0
        for i in xrange(0, len(self.todayLogoutTime), 2):
            delta += self.todayLogoutTime[i+1] - self.todayLogoutTime[i]
        self.monthActiveTime[idx] = delta
        return delta

    def add_online_time(self, idx, delta):
        self.monthActiveTime[idx] += delta

    def get_online_time(self, days):
        delta = 0
        self.get_today_online_time()
        for i in xrange(-days, 0):
            delta += self.monthActiveTime[i]
        return delta

    def add_today_logintime(self):
        self.todayLoginCount += 1

    def add_today_logouttime(self, t):
        self.todayLogoutTime.append(t)

    def add_rank(self, idx, r):
        self.monthRank[idx] = r

    def add_money(self, idx, c):
        self.money[idx] += c
        if self.isconsumer < 0: self.isconsumer = -idx - 1

    def set_createdtime(self, nflag=0):
        self.newCreateFlag = nflag
