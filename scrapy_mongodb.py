"""
scrapy-mongodb - MongoDB pipeline for Scrapy

Homepage: https://github.com/sebdah/scrapy-mongodb
Author: Sebastian Dahlgren <sebastian.dahlgren@gmail.com>
License: Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

Copyright 2013 Sebastian Dahlgren

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.read_preferences import ReadPreference

from scrapy import log
from scrapy.conf import settings


def not_set(string):
    """
    Check if a string is None or ''

    Returns True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False


class MongoDBPipeline():
    """
    MongoDB pipeline class
    """
    def __init__(self):
        """
        Constructor
        """
        #
        # Set default settings if they are not provided by the user
        #
        if not_set(settings['MONGODB_HOST']):
            mongodb_host = 'localhost'
        else:
            mongodb_host = settings['MONGODB_HOST']

        if not_set(settings['MONGODB_PORT']):
            mongodb_port = 27017
        else:
            mongodb_port = settings['MONGODB_PORT']

        if not_set(settings['MONGODB_FSYNC']):
            mongodb_fsync = False
        else:
            mongodb_fsync = settings['MONGODB_FSYNC']

        if not_set(settings['MONGODB_REPLICA_SET']):
            #
            # Connecting to a MongoDB replica set
            #

            # Check forced replication
            if not_set(settings['MONGODB_REPLICA_SET_W']):
                mongodb_rs_w = 0
            else:
                mongodb_rs_w = settings['MONGODB_REPLICA_SET_W']

            connection = MongoReplicaSetClient(
                '%s:%i' % (
                    settings['MONGODB_HOST'],
                    settings['MONGODB_PORT']),
                w=mongodb_rs_w,
                fsync=mongodb_fsync,
                read_preference=ReadPreference.PRIMARY_PREFERRED)

        else:
            #
            # Connecting to a stand alone MongoDB
            #
            connection = MongoClient(
                host=mongodb_host,
                port=mongodb_port,
                fsync=mongodb_fsync,
                read_preference=ReadPreference.PRIMARY)

        # Set up the collection
        database = connection[settings['MONGODB_DATABASE']]
        self.collection = database[settings['MONGODB_COLLECTION']]
        log.msg('Connected to MongoDB %s:%i, using "%s/%s"' % (
            mongodb_host,
            mongodb_port,
            settings['MONGODB_DATABASE'],
            settings['MONGODB_COLLECTION']))

        # Set the unique key if needed
        if not_set(settings['MONGODB_UNIQUE_KEY']):
            self.unique_key = None
        else:
            self.unique_key = settings['MONGODB_UNIQUE_KEY']

        # Ensure unique index
        if self.unique_key:
            self.collection.ensure_index(self.unique_key, unique=True)
            log.msg('Ensuring index for key %s' % self.unique_key)

    def process_item(self, item, spider):
        """
        Process the item and add it to MongoDB
        """
        if self.unique_key is None:
            self.collection.insert(dict(item))
        else:
            self.collection.update(
                {
                    self.unique_key: item[self.unique_key]
                },
                dict(item),
                upsert=True)
        log.msg('Item wrote to MongoDB database %s/%s' % (
            settings['MONGODB_DATABASE'],
            settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item
