from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING

client = MongoClient('127.0.0.1', 27017)
db_name = 'wangtiejiang'
db = client[db_name]
collection_useraction = db['account']
collection_password = db['passwd']
#
# # collection_useraction.insert({'用户名':'hahaha111','年龄':'18','电话':'11111'})
# # collection_useraction.insert({'用户名':'hahaha222','年龄':'28','电话':'22222'})
# # collection_useraction.insert({'用户名':'hahaha333','年龄':'38','电话':'33333'})
collection_useraction.insert({'_id': 1 ,'用户名':'hahaha444','年龄':'48','电话':'44444'})
#
# # for item in collection_useraction.find().sort('电话'):
# #     print(item['用户名'])
#
# a = collection_useraction.find_one({'用户名':'hahaha333'})
# print(a)
#
# # collection_useraction.remove({'用户名':'hahaha444'})
# #
for item in collection_useraction.find():
    print(item)
#
# #collection_password.insert({'密码':'654321'})
# #passwd_result = collection_password.find()
# # collection_password.update({'密码': '654321'},{'$set': 'xilanhua'})
# for i in collection_password.find():
#     print(i)
