import config, util
import os, time, datetime

def run(game_id, server_id, log_name, req, args):
    '''
    /rest/debug
    args:
        on = desc, temp, ...
        action = list, read, delete(only can delete temp)
    '''
    desc_path = config.LOG_DIR + '/' + game_id + '/desc/'
    path = config.LOG_DIR + '/' + game_id + '/' + server_id
    onfield = args.get('on')
    action = args.get('action')
    if action == 'list':
        temp = []
        try:
            temp += os.listdir(config.LOG_DIR + '/' + game_id + '/')
            temp += ['-----------------']
            temp += os.listdir(desc_path)
            temp += ['-----------------']
            temp += os.listdir(path)
            temp += ['-----------------']
            temp += os.listdir(path + '/temp/')
            temp += ['-----------------']
            temp2 = os.listdir('./')
            for tf in temp2:
                temp.append(tf + ': ' + str(datetime.datetime.fromtimestamp(os.path.getmtime('./' + tf))))
        except:
            pass
        req.write('\n'.join(temp))
    elif action == 'read':
        f = file(config.LOG_DIR + '/' + game_id + '/' + onfield)
        with f:
            lines = f.readlines()
            req.write(''.join(lines))
    elif action == 'delete':
        if os.path.isfile(path + '/temp/' + onfield):
            os.remove(path + '/temp/' + onfield)
    req.finish()
