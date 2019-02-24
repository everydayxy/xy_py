#while True:
#    try:
#        x = input('first num: ')
#        y = input('second number: ')
#        value = int(x)/int(y)
#        print(value)
#    except Exception as e:
#        print('except: %s' % e)
#    else:
#        break

#try:
#    1/0
#except NameError:
#    print('oops !! zero')
#else:
#    print('everything is ok')
#finally:
#    print('clean up')

while True:
    try:
        x = input('first num: ')
        y = input('second number: ')
        value = float(x)/float(y)
        print(value)
    except ZeroDivisionError:
        print('second number can\'t be zero!')
    except TypeError as T:
        print('it wasn\'t a number,was it ?')
        print(T)
    except:
        print('unknow happend')
    else:
        print('it\'s ok')
        break
