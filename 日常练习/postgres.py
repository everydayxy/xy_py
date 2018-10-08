# -*- coding: utf-8 -*-
import psycopg2

conn = psycopg2.connect(host="db", port=5432, user="postgres", database="naughty")
cur = conn.cursor()
sql = "select t1.account_id,t1.diamond, split_part(split_part(t2.item_str,';',1),',',2) as bank1,split_part(split_part(t2.item_str,';',2),',',2) as bank2,split_part(split_part(t2.item_str,';',3),',',2) as bank3 from roles t1 left join banks t2 on t1.account_id=t2.id;"
cur.execute(sql)

for i in cur.fetchall():
    a = i[0]
    b = i[1]
    c = i[2]
    d = i[3]
    e = i[4]

    if type(a) == type(None):
        a = 0
    elif type(b) == type(None):
        b = 0
    elif type(c) == type(None):
        c = 0
    elif type(d) == type(None):
        d = 0
    elif type(e) == type(None):
        e = 0

    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    e = int(e)


    print(a,b,c,d,e)



#conn.commit()  # 查询时无需，此方法提交当前事务。如果不调用这个方法，无论做了什么修改，自从上次调用#commit()是不可见的
conn.close()



