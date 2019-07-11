

slots = []
slots_num = 32

for _ in range(slots_num):
    slots.append([])


def put(slots,key,value):
    idx = -100
    index = hash(key) % slots_num
    try:
        for idx, (k,v) in enumerate(slots[index]):
            if k == key :
                break
        else:
            slots[index].append((key, value))

        if idx >= 0:
            slots[index][idx] = (key,value)

    except ValueError:
        slots[index] = (key,value)


put(slots,'x',1)
put(slots,'y',1)
put(slots,'y',2)
put(slots,'y',3)

print(slots)

