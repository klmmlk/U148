import os

from pymongo import MongoClient

# 创建一个 MongoClient 对象
client = MongoClient(os.getenv('MONGODB_URI'), )

# 获取数据库，如果数据库不存在，那么它将会被创建
db = client['u148']
# db.create_collection('config')
# 获取集合（表）
INFO_COLLECTION = db['article']
