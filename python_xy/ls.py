import argparse
import os
import sys
import stat

reload(sys)
sys.setdefaultencoding('utf8')


def list_dir(filepath):
    # item = []
    person_dir = next(os.walk(filepath))
    dir_and_file_names = person_dir[1] + person_dir[2]
    # for item1 in sorted(dir_and_file_names):
    #     if not item1.startswith('.'):
    #         item.append('{}/{}'.format(filepath,item1))
    # return item
    return ('{}/{}'.format(filepath,item) for item in sorted(dir_and_file_names) if not item.startswith('.'))

def get_size(filepath):
    if not args.human:
        return os.stat(filepath).st_size
    units = ['','K','M','G','T']
    idx = 0
    size = os.stat(filepath).st_size
    while size > 1024:
        size /= 1024.0
        idx += 1
    return '{:.1f}{}'.format(size,units[idx])

def permissions_to_unix_name(filepath):
    st = os.stat(filepath)
    is_dir = 'd' if stat.S_ISDIR(st.st_mode) else '-'
    dic = {'7':'rwx', '6' :'rw-', '5' : 'r-x', '4':'r--', '0': '---'}
    perm = str(oct(st.st_mode)[-3:])
    return is_dir + ''.join(dic.get(x,x) for x in perm)

def long_format(filepath):
    longformat = {
        'permisson': permissions_to_unix_name(filepath),
        'size': get_size(filepath),
        'file': filter_last(filepath)
    }
    return '{} {} {}'.format(
        longformat['permisson'],
        longformat['size'],
        longformat['file']
    )

def filter_last(filepath):
    if '/' in filepath:
        return filepath.split('/')[-1]
    else:
        return filepath

def main():
    for filepath in args.path:
        for new_item in list_dir(filepath):
            if not args.longformat and not args.human:
                print(filter_last(new_item))
            if args.longformat or args.human:
                print('{}'.format(long_format(new_item)))

if __name__ == '__main__':
    parse = argparse.ArgumentParser(add_help=False)
    parse.add_argument('-l', dest='longformat', help='long format', action='store_true')
    parse.add_argument('-h', dest='human', help='human readable', action='store_true')
    parse.add_argument('path', nargs='*', default='.')
    args = parse.parse_args()
    main()

