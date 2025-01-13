#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Mongo Database Connection Class
import motor.motor_asyncio

from build_config import *  
from util.log_util import Log


class MongoMixin(object):
    try:
        databases = [project['database'] for project in CONFIG['projects']]
        for db_config in databases:
            for db in db_config:
                client = motor.motor_asyncio.AsyncIOMotorClient(
                    db['host'],
                    db['port'],
                )
                user_db = client[db['key']]
                client = None 
                Log.i('MONGO', '{} has been Initialized!'.format(db['key']))
    except Exception as e:
        user_db = None
        Log.e('MONGO', f'Database Initialization Failed! Error: {e}')
