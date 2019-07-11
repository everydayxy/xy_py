import ConfigParser, os

CONFIG_FILE_NAME = '/etc/qlog/qlog.conf'

SERVER_ADDRESS = ''
SERVER_PORT = 80
SERVER_BACKLOG = 2000
THREAD_NUM = 8
LOG_DIR = '/opt/glog'

if os.path.isfile(CONFIG_FILE_NAME):
    cfg = ConfigParser.ConfigParser()
    cfg.read(CONFIG_FILE_NAME)
    if cfg.has_option('server', 'address'):
        SERVER_ADDRESS = cfg.get('server', 'address')
    if cfg.has_option('server', 'port'):
        SERVER_PORT = cfg.getint('server', 'port')
    if cfg.has_option('server', 'backlog'):
        SERVER_BACKLOG = cfg.get('server', 'backlog')
