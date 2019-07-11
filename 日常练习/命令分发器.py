def main():
    command_map_dict = dict()

    def command_map(command_str=None):
        def wrap(fn):
            command_map_dict.update({str(command_str): fn})
            # def wrapper(*args,**kwargs):
            #     ret = fn(*args,**kwargs)
            #     return ret
            # return wrapper
            return fn
        return wrap

    def interactive():
        while True:
            # print(command_map_dict)
            command = input('>>: ')
            if command in command_map_dict.keys():
                command_map_dict.get(command)()
            else:
                print('No such command')

    return interactive, command_map


interactive , command_map = main()


@command_map('ls')
def ls():
    print('ls')


@command_map('cmd')
def cmd():
    print('cmd')


@command_map('add')
def add():
    print('add')


interactive()