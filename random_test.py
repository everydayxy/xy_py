import random

def create_random_number(num):

    code = ''

    for i in range(0, num):
        choice = random.randint(0, 2)

        if choice == 0:
            tmp = chr(random.randint(65, 90))
        elif choice == 1:
            tmp = chr(random.randint(97, 122))
        elif choice == 2:
            tmp = random.randint(0, 9)

        code += str(tmp)

    return code

num = 10
code = create_random_number(num)
print(code)