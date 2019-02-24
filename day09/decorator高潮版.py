

user,passwd = 'xiayang','123456'

def auth(auth_type):
    print('auth type is %s ' % auth_type)
    def outer_wrapper(func):
        def wrapper(*args,**kargs):
            if auth_type == 'local':
                username = input('Please input username: ').strip()
                password = input('Please input pasword: ').strip()
                if user == username and passwd == password:
                    print('Login success!! ')
                    ret = func(*args,**kargs)
                    return ret
                else:
                    exit('Sorry , Login fail!!')
            elif auth_type == 'ldap':
                print('ldap function')
        return wrapper
    return outer_wrapper

def index():
    print('welcome to index')
@auth(auth_type='local')
def bbs():
    print('welcome to bbs')
    return 'from bbs'

index()
a = bbs()

print(a)