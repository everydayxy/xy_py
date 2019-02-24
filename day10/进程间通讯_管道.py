from multiprocessing import Pipe,Process

def aaa(conn):
    conn.send([None,'aaa',111])
    conn.send([None,'aaa',222])
    print(conn.recv())
    conn.close()


if __name__ == '__main__':
    parent_conn,child_process = Pipe()
    p = Process(target=aaa,args=(child_process,))
    p.start()
    print(parent_conn.recv())
    print(parent_conn.recv())
    parent_conn.send('greeting from parent')
    p.join()