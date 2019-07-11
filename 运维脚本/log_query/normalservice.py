from rolestructure import *
from readdata import *
import datetime, time, os
from dateutil.relativedelta import relativedelta
import json

services = ['active_day', 'seq_active_day', 'user_count', 'user_count_rank',
            'newuser_lost_ratio_week', 'newuser_lost_ratio_biweek','newuser_lost_ratio_month', 'newuser_count',
            'user_lost_ratio_week', 'user_lost_ratio_rank', 'user_lost_ratio_biweek', 'user_lost_ratio_month', 'user_back_ratio_week', 'user_back_ratio_biweek',
            'online_time', 'online_count', 'average_online_time', 'rank_online_time', 'login_count', 'logout_count',
            'consumer_summary', 'consumer_behavior_lost_ratio_week', 'consumer_behavior_lost_ratio_biweek', 'consumer_behavior_lost_ratio_month', 'consumer_behavior_count', 'consumer_behavior_rank']

#it works with filter functions
usertypes = {'allusers':0, 'newusers':1, 'activeusers':2, 'new_activeusers':3, 'consumers':4, 'non-consumers': 5}

def compare(role1, role2):
    if role1.name == role2.name: return 0
    elif role1.name < role2.name: return -1
    else: return 1

class NormalStatisticService:

    EFFECTIVE_USER_DAYS = 5
    MAXLENGTH = 64
    SEPARATOR = '|'
    MAXLEVEL = 200

    def __init__(self):
        self.tables = {}
        self.roles = {}
        self.dayslimit = 7
        self.timeoffset = 8

    def get_table_definition(self, descpath, path):
        if os.path.isfile('./config.json') == False:
            return False
        f = file('config.json')
        with f:
            lines = f.readlines()
            try:
                logdict = json.loads(' '.join([line.strip() for line in lines]))
            except:
                return False
        try:
            temp = descpath.split('/')
            gameid = temp[-2] if temp[-1] != '' else temp[-3]
            temp = path.split('/')
            serverid = temp[-1] if temp[-1] != '' else temp[-2]
        except:
            return False
        if gameid not in logdict:
            gameid = 'wly'
        try:
            for k in logdict[gameid][1]:
                for prefix in logdict[gameid][1][k]:
                    if prefix in serverid:
                        self.timeoffset = int(k)
                        break
        except:
            pass
        logconfig = logdict[gameid][0]
        for log in logconfig:
            try:
                f = file(descpath + '/' + logconfig[log][0])
            except:
                continue
            lines = f.readlines()
            self.tables[str(log)] = [str(logconfig[log][0])]
            for i in xrange(1, len(logconfig[log])):
                item = logconfig[log][i]
                try:
                    self.tables[str(log)].append(lines.index(item+'\n'))
                except:
                    print "error: ", logconfig[log][0]
                    return False
            f.close()
        return True

    def get_roles_info(self, descpath, path, startdate, enddate=None, onfield='active_day', groupby='allusers'):
        to = TimeOperation()
        if self.get_table_definition(descpath, path) == False or len(self.tables.keys()) == 0:
            return 'Description files disappeared!'
        if enddate != None:
            fdates = to.getperiod(startdate, enddate, '%Y-%m-%d', None)
        else:
            fdates = [to.strtodate(startdate, '%Y-%m-%d')]
            if fdates[0] == None: del fdates[0]

        if len(fdates) == 0: return 'Date period was not specified!'

        if 'newuser_lost_ratio' in onfield or 'user_lost_ratio' in onfield or \
        'consumer_behavior_lost_ratio' in onfield:
            if onfield.endswith('biweek'): self.dayslimit = 14
            elif onfield.endswith('month'): self.dayslimit = 30
            else: self.dayslimit = 7
            for i in xrange(self.dayslimit):
                fdates.append(fdates[-1] + relativedelta(days=1))
        elif 'user_back_ratio' in onfield:
            if onfield.endswith('biweek'): self.dayslimit = 28
            elif onfield.endswith('month'): self.dayslimit = 60
            else: self.dayslimit = 14
            for i in xrange(self.dayslimit):
                fdates.append(fdates[-1] + relativedelta(days=1))

        if len(fdates) >= self.MAXLENGTH:
            return 'Date period exceeded!'

        if onfield == 'seq_active_day': seqflag = True
        else: seqflag = False

        flag = 0
        for days in xrange(min(8, len(fdates))):
            for j in xrange(-days, min(8, len(fdates)+1)):
                fname = path + '/temp/' + to.datetostr(fdates[-(days+1)], '%Y-%m-%d') + '-' + str(len(fdates)+j) + '.txt'
                if os.path.isfile(fname):
                    flag = 1
                    break
            if flag == 1: break
        if flag == 1:
            self.load(fname)
            if days > 0:
                self.traverse(lambda role: role.add_day(days))
            elif fdates[-1] >= datetime.datetime.now() - relativedelta(days=1):
                days = 1
        else:
            days = len(fdates)

        if days > 0:
            idx = -days
            mask = 1 << (days-1)
            for i in xrange(days, 0, -1):
                fpath = path + '/' + to.datetostr(fdates[idx], '%Y-%m-%d') + '/'
                #get role create information
                self.get_role_create_info(fpath, mask, i-1)
                #get role login, logout information
                if idx == -1: self.get_role_login_info(fpath, mask, idx)
                self.get_role_logout_info(fpath, mask, idx, fdates[idx]+datetime.timedelta(0,24*3600-1))
                self.get_role_money_info(fpath, mask, idx)
                mask >>= 1
                idx += 1
            fpath = path + '/' + to.datetostr(fdates[-1]+relativedelta(days=1), '%Y-%m-%d') + '/'
            self.get_role_logout_info(fpath, 1, -1, fdates[-1]+datetime.timedelta(0,24*3600-1))
            if os.path.exists(path + '/temp/') == False:
                os.mkdir(path + '/temp/')
            self.save(path + '/temp/' + to.datetostr(fdates[-1], '%Y-%m-%d') + '-' + str(len(fdates)) + '.txt')

        #delete .txt files which created earlier than 30 days
        txtfiles = os.listdir(path + '/temp/')
        dt = datetime.datetime.now() - relativedelta(days=30, hours=8)
        for tf in txtfiles:
            if datetime.datetime.fromtimestamp(os.path.getmtime(path + '/temp/' + tf)) < dt:
                os.remove(path + '/temp/' + tf)
        return self.compute_roles_statistics(len(fdates), seqflag, onfield, groupby)

    def compute_roles_statistics(self, days=7, seqflag=False, onfield='active_day', groupby='allusers'):
        ret_list = []
        if onfield == 'active_day' or onfield == 'seq_active_day':
            #get role login, logout information
            self.traverse(self.get_role_active_statistics_func(days, seqflag, usertypes.get(groupby, 0))[0])
            for i in range(1, days+1):
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.active_user_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, 1.0 * self.active_user_count[i]/(self.total_count+0.01)))
        elif onfield == 'newuser_count':
            #get role create information
            self.traverse(self.get_role_create_statistics_func(days, seqflag))
            for i in range(days):
                ret_list.append('%d%s%d' % (i, self.SEPARATOR, self.freshrole_total_count[i]))
        elif 'user_count' in onfield:
            #get role login, logout information
            self.traverse(self.get_role_active_statistics_func(days, seqflag, usertypes.get(groupby, 0))[3])
            if 'rank' in onfield:
                for i in xrange(1, self.MAXLEVEL):
                    if self.rank_count[i] == 0: continue
                    ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.rank_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, 1.0*self.rank_count[i]/(self.total_count+0.01)))
            else:
                for i in range(0, days):
                    ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.active_user_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, 1.0 * self.active_user_count[i]/(self.total_count+0.01)))
        elif 'newuser_lost_ratio' in onfield:
            #get role create information
            self.traverse(self.get_role_create_statistics_func(days, seqflag))
            for i in range(self.dayslimit, days):
                k = i - self.dayslimit
                t2 = self.freshrole_total_count[i]
                t1 = 0
                for j in range(0, i+1):
                    t1 = self.freshrole_active_count[i][j]
                    ret_list.append('%d%s%d%s%d%s%d%s%.3f' % (k, self.SEPARATOR, j, self.SEPARATOR, t1, self.SEPARATOR, t2, self.SEPARATOR, t1*1.0/(t2+0.01)))
        elif 'user_lost_ratio' in onfield:
            self.traverse(self.get_role_active_statistics_func(days, seqflag, usertypes.get(groupby, 0))[1])
            if 'rank' in onfield:
                for i in xrange(1, self.MAXLEVEL):
                    if self.rank_count[i] == 0: continue
                    ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.rank_count[i], self.SEPARATOR, self.week_lost_count, self.SEPARATOR, 1.0*self.rank_count[i]/(self.week_lost_count+0.01)))
            else:
                ret_list.append('%d%s%d%s%.3f' % (self.week_lost_count, self.SEPARATOR, self.week_total_count, self.SEPARATOR, 1.0 * self.week_lost_count / (self.week_total_count+0.01)))
        elif 'user_back_ratio' in onfield:
            self.traverse(self.get_role_active_statistics_func(days, seqflag, usertypes.get(groupby, 0))[2])
            ret_list.append('%d%s%d%s%.3f' % (self.week_back_count, self.SEPARATOR, self.week_lost_count, self.SEPARATOR, 1.0 * self.week_back_count / (self.week_lost_count+0.01)))
        elif onfield == 'online_time':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[0])
            for i in range(0, 10*days, 1):
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.online_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, self.online_count[i] * 1.0 / (self.total_count+0.01)))
        elif onfield == 'online_count':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[1])
            for i in range(0, 288):
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.online_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, self.online_count[i] * 1.0 / (self.total_count+0.01)))
        elif onfield == 'average_online_time':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[2])
            ret_list.append('%.3f%s%d%s%.3f' % (self.online_time[0]*1.0/60, self.SEPARATOR, self.login_count[0], self.SEPARATOR, 1.0 * self.online_time[0] / max(self.login_count[0]*60, 1)))
        elif onfield == 'rank_online_time':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[3])
            for i in xrange(1, self.MAXLEVEL):
                if self.online_time[i] == 0: continue
                ret_list.append('%d%s%.3f%s%d%s%.3f' % (i, self.SEPARATOR, self.online_time[i]*1.0/60, self.SEPARATOR, self.login_count[i], self.SEPARATOR, 1.0 * self.online_time[i] / max(self.login_count[i]*60, 1)))
        elif onfield == 'login_count':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[4])
            for i in xrange(self.MAXLEVEL):
                if self.login_count[i] == 0: continue
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.login_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, 1.0 * self.login_count[i] / (self.total_count+0.01)))
            for item in self.extrodinary_login:
                ret_list.append(str(item[0]) + self.SEPARATOR + str(item[1]))
        elif onfield == 'logout_count':
            self.traverse(self.get_role_online_statistics_func(days, usertypes.get(groupby, 0))[5])
            for i in xrange(self.MAXLEVEL):
                if self.login_count[i] == 0: continue
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.login_count[i], self.SEPARATOR, self.total_count, self.SEPARATOR, 1.0 * self.login_count[i] / (self.total_count+0.01)))
            for item in self.extrodinary_login:
                ret_list.append(str(item[0]) + self.SEPARATOR + str(item[1]))
        elif onfield == 'consumer_summary':
            self.traverse(self.get_role_money_statistics_func(days)[0])
            for i in xrange(days):
                temp = [i, self.money[i], self.consumer_count[i], 1.0*self.money[i]/max(self.consumer_count[i],1),
                        self.active_user_count[i], 1.0*self.consumer_count[i]/(self.active_user_count[i]+0.01),
                        self.new_consumer_count[i], self.total_consumer_count, self.total_user_count]
                ret_list.append(self.SEPARATOR.join([str(item) for item in temp]))
        elif 'consumer_behavior_lost_ratio' in onfield:
            self.traverse(self.get_role_money_statistics_func(days)[1])
            temp = self.total_user_count-self.total_consumer_count
            ret_list.append('%d%s%d%s%.3f' % (temp, self.SEPARATOR, self.total_user_count, self.SEPARATOR, 1.0*temp/(self.total_user_count+0.01)))
        elif onfield == 'consumer_behavior_count':
            self.traverse(self.get_role_money_statistics_func(days)[2])
            for i in xrange(1, days+1):
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.consumer_count[i], self.SEPARATOR, self.total_consumer_count, self.SEPARATOR, 1.0*self.consumer_count[i]/(self.total_consumer_count+0.01)))
        elif onfield == 'consumer_behavior_rank':
            self.traverse(self.get_role_money_statistics_func(days)[3])
            for i in xrange(1, self.MAXLEVEL):
                if self.rank_count[i] == 0: continue
                ret_list.append('%d%s%d%s%d%s%.3f' % (i, self.SEPARATOR, self.rank_count[i], self.SEPARATOR, self.total_consumer_count, self.SEPARATOR, 1.0*self.rank_count[i]/(self.total_consumer_count+0.01)))
        return '\n'.join(ret_list)

    def get_role_create_info(self, fpath, mask, days):
        if 'CreateRole' not in self.tables < 3: return
        do = DataOperation()
        to = TimeOperation()
        result = do.read_data_file(fpath + self.tables['CreateRole'][0] + '.dat', '|', self.tables['CreateRole'][1:])
        for r in result:
            if ' ' in r[0]: continue
            name = r[0]
            role = self.roles.get(name, None)
            if role == None:
                role = Role(name, days)
                role.mark_active(mask)
                self.roles[name] = role

    def get_role_login_info(self, fpath, mask, days):
        if 'RoleLogin' not in self.tables: return
        do = DataOperation()
        to = TimeOperation()
        result = do.read_data_file(fpath + self.tables['RoleLogin'][0] + '.dat', '|', self.tables['RoleLogin'][1:])
        for r in result:
            if ' ' in r[0]: continue
            name = r[0]
            role = self.roles.get(name, None)
            if role == None:
                role = Role(name, self.MAXLENGTH)
                self.roles[name] = role
            role.mark_active(mask)
            if days == -1: role.add_today_logintime()

    def get_role_logout_info(self, fpath, mask, days, deadline):
        if 'RoleLogout' not in self.tables: return
        do = DataOperation()
        to = TimeOperation()
        result = do.read_data_file(fpath + self.tables['RoleLogout'][0] + '.dat', '|', self.tables['RoleLogout'][1:])
        startpoint = deadline - relativedelta(days=1)
        for r in result:
            if ' ' in r[0]: continue
            name = r[0]
            try:
                t1 = to.strtodate(r[1], '%Y-%m-%d %H:%M:%S') + relativedelta(hours=self.timeoffset)
                t2 = to.strtodate(r[2], '%Y-%m-%d %H:%M:%S')
                rank = int(r[-1])
                if t1 == None or t2 == None or rank >= self.MAXLEVEL: continue
            except:
                continue
            role = self.roles.get(name, None)
            if role == None:
                role = Role(name, self.MAXLENGTH)
                self.roles[name] = role
            role.mark_active(mask)
            if t1 > deadline: break
            if t2 > deadline: t2 = deadline
            if t1 <= startpoint and t2 > startpoint:
                if 1-days < self.MAXLENGTH:
                    delta = startpoint-t1
                    role.add_online_time(days-1, delta.days*24*3600 + delta.seconds + 1)
                    role.add_rank(days-1, rank)
                t1 = startpoint + datetime.timedelta(0, 1)
            if days == -1:
                try:
                    delta = t1 - startpoint
                    role.add_today_logouttime(delta.days*24*3600 + delta.seconds - 1)
                    delta = t2 - startpoint
                    role.add_today_logouttime(delta.days*24*3600 + delta.seconds - 1)
                except:
                    if len(role.todayLogoutTime) % 2 == 1:
                        del role.todayLogoutTime[-1]
                    print role.name, t1, t2, 'error'
            delta = t2 - t1
            role.add_online_time(days, delta.days*24*3600 + delta.seconds + 1)
            role.add_rank(days, rank)

    def get_role_money_info(self, fpath, mask, days):
        if 'Money' not in self.tables: return
        do = DataOperation()
        to = TimeOperation()
        result = do.read_data_file(fpath + self.tables['Money'][0] + '.dat', '|', self.tables['Money'][1:])
        for r in result:
            if ' ' in r[0]: continue
            name = r[0]
            role = self.roles.get(name, None)
            if role == None:
                role = Role(name, self.MAXLENGTH)
                self.roles[name] = role
            role.mark_active(mask)
            try:
                role.add_money(days, int(r[1]))
            except:
                pass

    def get_role_active_statistics_func(self, days, seqflag=False, usertype=0):
        self.active_user_count = [0] * self.MAXLENGTH
        self.total_count = 0
        self.week_lost_count = 0
        self.week_total_count = 0
        self.week_back_count = 0
        self.rank_count = [0] * self.MAXLEVEL
        mask = (1 << days)-1
        effective_mask = (1 << self.EFFECTIVE_USER_DAYS) - 1

        def filter_users(role):
            if usertype == 0: return True
            if usertype == 1: #new created users
                return role.newCreateFlag < days
            if usertype == 2: #effective users
                if role.newCreateFlag > self.EFFECTIVE_USER_DAYS:
                    if role.newCreateFlag >= days: return True
                    active_flag = role.get_active(mask)
                    active_flag >>= (role.newCreateFlag-self.EFFECTIVE_USER_DAYS+1)
                    return active_flag == effective_mask
            if usertype == 3:
                if role.newCreateFlag > self.EFFECTIVE_USER_DAYS:
                    if role.newCreateFlag >= 30: return False
                    active_flag = role.get_active(mask)
                    active_flag >>= (role.newCreateFlag-self.EFFECTIVE_USER_DAYS+1)
                    return active_flag == effective_mask
            if usertype == 4:
                return role.isconsumer >= 0
            if usertype == 5:
                return role.isconsumer < 0
            return False

        def func(role):
            if filter_users(role) == False: return
            sum = func2(role)
            if sum > 0:
                self.active_user_count[sum] += 1
                self.total_count += 1

        def lost_func(role):
            if filter_users(role) == False: return
            temp = func4(role)
            if temp > 0:
                self.week_total_count += 1
            if temp == 2:
                self.week_lost_count += 1
                self.rank_count[max(role.monthRank)] += 1

        def back_func(role):
            if filter_users(role) == False: return
            temp = func5(role)
            if temp > 0:
                self.week_lost_count += 1
            if temp == 2:
                self.week_back_count += 1

        def user_count_func(role):
            if filter_users(role) == False: return
            self.total_count += 1
            self.rank_count[max(role.monthRank)] += 1
            func3(role)

        def func2(role):
            active_flag = role.get_active(mask)
            sum = 0
            if active_flag & 1 == 0: return 0
            if seqflag == False:
                while active_flag > 0:
                    if active_flag & 1 == 1: sum += 1
                    active_flag >>= 1
            else:
                temp = 0
                while True:
                    if active_flag & 1 == 1:
                        temp += 1
                    else:
                        if sum < temp: sum = temp
                        temp = 0
                    if active_flag == 0: break
                    active_flag >>= 1
            return sum

        def func3(role):
            active_flag = role.get_active(mask)
            sum = 0
            while active_flag > 0:
                if active_flag & 1 == 1:
                    self.active_user_count[sum] += 1
                sum += 1
                active_flag >>= 1
            return sum

        def func4(role):
            mask1 = 2**(self.dayslimit)-1
            mask2 = (2**(days-self.dayslimit)-1) << self.dayslimit
            flag1 = role.get_active(mask1)
            flag2 = role.get_active(mask2)
            if (flag2 > 0) and (flag1 == 0):
                return 2
            elif flag2 > 0:
                return 1
            return 0

        def func5(role):
            mask1 = 2**(self.dayslimit/2)-1
            mask2 = mask1 << (self.dayslimit/2)
            mask3 = (2**(days-self.dayslimit)-1) << self.dayslimit
            flag1 = role.get_active(mask1)
            flag2 = role.get_active(mask2)
            flag3 = role.get_active(mask3)
            if (flag3 > 0) and (flag1 > 0) and (flag2 == 0):
                return 2
            elif flag3 > 0 and flag2 == 0:
                return 1
            return 0

        return func, lost_func, back_func, user_count_func, func2, filter_users

    def get_role_online_statistics_func(self, days, usertype=0):
        self.online_count = [0] * (max(10*days, 288))
        self.total_count = 0
        self.login_count = [0] * self.MAXLEVEL
        self.online_time = [0] * self.MAXLEVEL
        self.extrodinary_login = []
        mask = (1 << days)-1

        filter_func = self.get_role_active_statistics_func(days, False, usertype)[5]

        def online_time_func(role):
            if filter_func(role) == False: return
            if role.get_active(mask) == 0: return
            delta = role.get_online_time(days)
            try:
                self.online_count[delta / 3600] += 1
            except:
                self.online_count[10*days-1] += 1
            self.total_count += 1

        def online_count_func(role):
            if filter_func(role) == False: return
            if role.get_active(1) == 0: return
            for i in range(0, len(role.todayLogoutTime), 2):
                s = role.todayLogoutTime[i] / 300
                delta = role.todayLogoutTime[i+1] - role.todayLogoutTime[i]
                e = delta / 300 + s + 1
                for j in range(s, e):
                    self.online_count[j] += 1
            self.total_count += 1

        def average_online_time_func(role):
            if filter_func(role) == False: return
            if role.get_active(1) == 0: return
            self.login_count[0] += len(role.todayLogoutTime)/2
            role.get_today_online_time()
            self.online_time[0] += role.monthActiveTime[-1]

        def rank_average_online_time_func(role):
            if filter_func(role) == False: return
            if role.get_active(1) == 0: return
            role.get_today_online_time()
            for i in xrange(-days, 0):
                self.online_time[role.monthRank[i]] += role.monthActiveTime[i]
                self.login_count[role.monthRank[i]] += 1

        def login_count_func(role):
            if filter_func(role) == False: return
            if role.get_active(1) == 0: return
            try:
                self.login_count[role.todayLoginCount] += 1
                self.total_count += 1
            except:
                self.extrodinary_login.append((role.name, role.todayLoginCount))

        def logout_count_func(role):
            if filter_func(role) == False: return
            if role.get_active(1) == 0: return
            try:
                self.login_count[len(role.todayLogoutTime)/2] += 1
                self.total_count += 1
            except:
                self.extrodinary_login.append((role.name, len(role.todayLogoutTime)/2))

        return online_time_func, online_count_func, average_online_time_func, rank_average_online_time_func, login_count_func, logout_count_func

    def get_role_money_statistics_func(self, days):
        self.active_user_count = [0] * self.MAXLENGTH
        self.consumer_count = [0] * self.MAXLENGTH
        self.new_consumer_count = [0] * self.MAXLENGTH
        self.money = [0] * self.MAXLENGTH
        self.total_user_count = 0
        self.total_consumer_count = 0
        self.rank_count = [0] * self.MAXLEVEL
        mask = (1 << days)-1

        def summary_func(role):
            flag = role.get_active(mask)
            if flag == 0: return
            self.total_user_count += 1
            if role.isconsumer >= 0:
                self.total_consumer_count += 1
                if role.isconsumer < days: self.new_consumer_count[role.isconsumer] += 1
            idx = 0
            while flag > 0:
                if flag & 1 == 1:
                    self.active_user_count[idx] += 1
                    if role.money[-idx-1] > 0:
                        self.consumer_count[idx] += 1
                        self.money[idx] += role.money[-idx-1]
                flag >>= 1
                idx += 1

        def remained_func(role):
            if role.isconsumer >= self.dayslimit:
                self.total_user_count += 1
                for i in xrange(-self.dayslimit, 0):
                    if role.money[i] > 0:
                        self.total_consumer_count += 1
                        break

        def consumer_behavior_count_func(role):
            if role.isconsumer < days and role.isconsumer >= 0:
                self.total_consumer_count += 1
                temp = 0
                for i in xrange(-days, 0):
                    if role.money[i] > 0:
                        temp += 1
                self.consumer_count[temp] += 1

        def consumer_behavior_rank_func(role):
            if role.isconsumer < days and role.isconsumer >= 0:
                for i in xrange(-days, 0):
                    if role.money[i] > 0:
                        self.rank_count[role.monthRank[i]] += 1
                        self.total_consumer_count += 1

        return summary_func, remained_func, consumer_behavior_count_func, consumer_behavior_rank_func

    def get_role_create_statistics_func(self, days, seqFlag = False):
        self.freshrole_active_count = [None] * (self.MAXLENGTH)
        self.freshrole_total_count = [0] * (self.MAXLENGTH)
        mask = (1 << days) - 1

        for i in xrange(days):
            self.freshrole_active_count[i] = [0] * (days+1)

        def func(role):
            if role.newCreateFlag < days:
                self.freshrole_total_count[role.newCreateFlag] += 1
                if role.newCreateFlag >= self.dayslimit:
                    sum = func2(role)
                    self.freshrole_active_count[role.newCreateFlag][sum] += 1

        def func2(role):
            active_flag = role.get_active(mask)
            sum = 0
            while active_flag > 0:
                if active_flag & 1 == 1: break
                sum += 1
                active_flag >>= 1
            return role.newCreateFlag - sum
        return func

    def save(self, fname):
        to = TimeOperation()
        fwriter = open(fname, 'w+')
        for k in self.roles:
            role = self.roles[k]
            fwriter.write('%s %d %d %d\n' % (str(role.name), role.newCreateFlag, role.monthActiveFlag, role.isconsumer))
            for i in xrange(self.MAXLENGTH):
                fwriter.write(str(role.monthActiveTime[i]) + ' ' + str(role.monthRank[i]) + ' ' + str(role.money[i]) + '\n')
            fwriter.write(str(role.todayLoginCount) + ' ' + str(len(role.todayLogoutTime)) + '\n')
            for t in role.todayLogoutTime:
                fwriter.write(str(t) + '\n')
        fwriter.close()

    def load(self, fname):
        to = TimeOperation()
        freader = open(fname)
        data = freader.readline().strip()
        while data != '':
            rname, nflag, mflag, isconsumer = data.strip().split()
            role = Role(rname, int(nflag))
            role.monthActiveFlag = int(mflag)
            role.isconsumer = int(isconsumer)
            for i in xrange(self.MAXLENGTH):
                data = freader.readline().split()
                role.monthActiveTime[i] = int(data[0])
                role.monthRank[i] = int(data[1])
                role.money[i] = int(data[2])
            ilen, olen = freader.readline().split()
            role.todayLoginCount = int(ilen)
            for i in xrange(int(olen)):
                data = freader.readline().strip()
                role.todayLogoutTime.append(int(data))
            self.roles[role.name] = role
            data = freader.readline().strip()
        freader.close()

    def traverse(self, func):
        for k in self.roles:
            func(self.roles[k])