import json

filename = 'store_file.json'
fb = open(filename,'r')
new_dict = json.loads(fb.read())

def new_delete():
    user = input('请输入需要删除的用户名：').strip('\r')
    for k,v in new_dict.items():
        if user == v["username"]:
            del new_dict[k]
            break
    else:
        print('您想删除的用户不存在')

def new_update():
    num_max = 0
    for k, v in new_dict.items():
        if int(k) > num_max:
            num_max = int(k)

    # if num_max == 0:
    #     print('无用户，请提交数据')
    num_max += 1
    print('输入格式： 用户名:年龄:联系方式')
    user,age,tel = input('>>> ').split(':')
    new_dict[str(num_max)] = {
      "username": user,
      "age":age,
      "tel":tel
          }


def new_find():
    user = input('请输入需要查找的用户名：')
    for k,v in new_dict.items():
        if user == v["username"]:
            print('用户名:{} 年龄:{} 电话:{}'.format(v["username"],v["age"],v['tel']))
            break
    else:
        print('用户没找到')

def new_show():
    if new_dict:
        print('{:>20} |{:>20} |{:>20}'.format('username', 'age', 'tel'))
        for k,v in new_dict.items():
            print('{:>20} |{:>20} |{:>20}'.format(v["username"],v["age"],v['tel']))
    else:
        print('目前啥都没有')

def new_exit():
    answer = input('请问您想保存现有信息并退出吗？？[y/n]')
    if answer == 'y' or answer == 'Y':
        with open(filename, 'w') as fb2:
            fb2.write(json.dumps(new_dict, indent=4, sort_keys=True, ensure_ascii=False))
        exit(0)


def main():
    while True:
        action = input(">>> ")
        if action == 'delete':
            new_delete()
        elif action == 'update':
            new_update()
        elif action == 'find':
            new_find()
        elif action == 'show':
            new_show()
        elif action == 'exit':
            new_exit()
        else:
            print('命令格式: [delete|update|find|show|exit]')

if __name__ == "__main__":
    main()