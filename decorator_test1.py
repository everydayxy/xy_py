

un,pw = 'alex','123456'

def auth(auth_type):
    print('auth func: ',auth_type)
    def outer_wrapper(func):
        def wrapper(*args,**kargs):
            print('wrapper func args: ',args,kargs)
            username = input('plz input username: ').strip()
            password = input('plz input password: ').strip()
            if auth_type == 'local':
                if un == username and pw == password:
                    print('\033[32;1m authen pass \033[32;0m')
                    ret = func(*args, **kargs)
                    return ret
                else:
                    exit('\033[31;1m authen fail \033[32;0m')
            elif auth_type == 'ldap':
                print('搞毛线ldap。。。。')

        return wrapper
    return outer_wrapper


@auth(auth_type='ldap')
def index():
    print('welcome to index page')
    return 'from index'
@auth(auth_type='local')
def bbs():
    print('welcome to bbs page')


a = index()
print(a)
b = bbs()
print(b)
