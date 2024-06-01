import os
from log_tool import Mylog
from pymongo import MongoClient
import json
logger = Mylog('CONFIG')
try:
    with open('./config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logger.log_message('config.json not found, please create one.')
    exit()
# 创建一个 MongoClient 对象
client = MongoClient(config.get('MONGO_URI'))

# 获取数据库，如果数据库不存在，那么它将会被创建
db = client['u148']
# db.create_collection('config')
# 获取集合（表）
INFO_COLLECTION = db['article']
USER_COLLECTION = db['user']