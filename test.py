import re

def add_zero(a):
    game,number = a.split('-')
    digital_split = []
    for v in number:
        digital_split.append(v)
    digital_split.insert(1,'0')
    digital = ''.join(digital_split)
    return game + '-' +  digital

print(add_zero('lequ-133'))