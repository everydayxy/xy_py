import os

import config, util
import computation as cp

def run(game_id, server_id, log_name, req, args):
    desc_path = config.LOG_DIR + '/' + game_id + '/desc/' + log_name
    if not os.path.isfile(desc_path):
        return req.finish()
    f = file(desc_path, 'r')
    lines = f.readlines()
    field_idx = dict()
    idx = 0
    for line in lines:
        line = line[0:-1]
        field_idx[line] = idx
        idx = idx + 1
    group_by = list()
    if args.has_key('group'):
        groups = args['group'].split(',')
        for group in groups:
            if not field_idx.has_key(group):
                print 'Invalid field name ' + group
                return req.finish()
            group_by.append(field_idx[group])
    start_date = util.parseDate(args.get('start_time'))
    end_date = util.parseDate(args.get('end_time'))
    dirs = util.listDirs(game_id, server_id, start_date, end_date)
    path = config.LOG_DIR + '/' + game_id + '/' + server_id
    final_data = dict()
    on = -1
    on_field = args.get('on')
    specialnodes, func = cp.generate_function_tree(on_field, field_idx)
    if func == None: return req.finish()
    ret_data = {}
    if len(group_by) == 0:
        ret_data[''] = [0] * (len(specialnodes) + 1)
        flag = True
    #if there are max, min, count, sum
    if len(specialnodes) > 0:
        for d in dirs:
            filename = path + '/' + d + '/' + log_name + '.dat'
            if not os.path.isfile(filename):
                continue
            f = file(filename, 'r')
            with(f):
                while True:
                    line = f.readline()[:-1]
                    if len(line) == 0: break
                    parts = line.split('|')
                    if len(parts) > len(field_idx.keys()): continue
                    temp = []
                    for item in parts:
                        try: temp.append(int(item))
                        except: temp.append(item)
                    key = str()
                    for idx in group_by:
                        key = key + parts[idx] + '|'
                    if key not in ret_data:
                        ret_data[key] = [0]*(len(specialnodes)+1)
                        flag = True
                    for i in xrange(len(specialnodes)):
                        sn = specialnodes[i][0]
                        if sn.name == 'min' and flag == True:
                            ret_data[key][i] = 9999999999
                        elif sn.name == 'count' and flag == True:
                            ret_data[key][i] = []
                        if sn.name == 'count':
                            ret_data[key][i] = sn.evaluate([temp, ret_data[key][i]])
                        else:
                            ret_data[key][i] = sn.evaluate([temp, [ret_data[key][i]]])
                    flag = False
    if cp.has_paramnode(func) == False:
        for key in ret_data:
            #adjust 'NA' nodes
            for i in xrange(len(specialnodes)):
                sn = specialnodes[i][1]
                sn.set_value(ret_data[key][i])
            ret_data[key][-1] = func.evaluate([])
    else:
        for d in dirs:
            filename = path + '/' + d + '/' + log_name + '.dat'
            if not os.path.isfile(filename):
                continue
            f = file(filename, 'r')
            with(f):
                while True:
                    line = f.readline()[:-1]
                    if len(line) == 0: break
                    parts = line.split('|')
                    if len(parts) > len(field_idx.keys()): continue
                    temp = []
                    for item in parts:
                        try: temp.append(int(item))
                        except: temp.append(item)
                    key = str()
                    for idx in group_by:
                        key = key + parts[idx] + '|'
                    #adjust 'NA' nodes
                    for i in xrange(len(specialnodes)):
                        sn = specialnodes[i][1]
                        sn.set_value(ret_data[key][i])
                    ret_data[key][-1] = func.evaluate(temp)
    for k, v in ret_data.iteritems():
        req.write(k + str(v[-1]) + '\n')
    return req.finish()
