# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2020-03-03
-------------------------------------------------
   Change Activity:
                   2020-03-03:
-------------------------------------------------
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from jktj.jktj import initHost
import redis

app = Flask(__name__)
app.config.from_object(Config())

appconfig = app.config

redis_pool = redis.ConnectionPool(host=appconfig['REDIS_HOST'], port=appconfig['REDIS_PORT'], decode_responses=True)
redis = redis.Redis(connection_pool=redis_pool)


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)
db = SQLAlchemy(app=app)

initHost(appconfig['SERVER_URL'])
