

def b64decode(data:str) -> bytes:
    table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    decoded = bytearray()
    s = 0
    for e in range(4,len(data),4):
        tmp = 0
        for i,c in enumerate(data[s:e]):
            if c != '=':
                tmp += table.index(c) << 24 - (i+1) * 6
            else:
                tmp += 0 << 24 - (i+1) * 6
        decoded.extend(tmp.to_bytes(3,'big'))
        s += 4
    return bytes(decoded.rstrip(b'\x00'))


print(b64decode('YWJjZa=='))
