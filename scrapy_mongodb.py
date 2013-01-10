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
    # Default options
    config = {
        'uri': 'mongodb://localhost:27017',
        'fsync': False,
        'write_concern': 0,
        'database': 'scrapy-mongodb',
        'collection': 'items',
        'replica_set': None,
        'unique_key': None,
    }

    def __init__(self):
        """
        Constructor
        """
        # Configure the connection
        self.configure()

        if self.config['replica_set'] is not None:
            connection = MongoReplicaSetClient(
                self.config['uri'],
                replicaSet=self.config['replica_set'],
                w=self.config['write_concern'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            # Connecting to a stand alone MongoDB
            connection = MongoClient(
                self.config['uri'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY)

        # Set up the collection
        database = connection[self.config['database']]
        self.collection = database[self.config['collection']]
        log.msg('Connected to MongoDB %s, using "%s/%s"' % (
            self.config['uri'],
            self.config['database'],
            self.config['collection']))

        # Ensure unique index
        if self.config['unique_key']:
            self.collection.ensure_index(self.config['unique_key'], unique=True)
            log.msg('Ensuring index for key %s' % self.config['unique_key'])

    def configure(self):
        """ Configure the MongoDB connection """
        # Handle deprecated configuration
        if not not_set(settings['MONGODB_HOST']):
            log.msg('DeprecationWarning: MONGODB_HOST is deprecated',
                level=log.WARNING)
            mongodb_host = settings['MONGODB_HOST']

            if not not_set(settings['MONGODB_PORT']):
                log.msg('DeprecationWarning: MONGODB_PORT is deprecated',
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://%s:%i' % (
                    mongodb_host, settings['MONGODB_PORT'])
            else:
                self.config['uri'] = 'mongodb://%s:27017' % mongodb_host

        if not not_set(settings['MONGODB_REPLICA_SET']):
            if not not_set(settings['MONGODB_REPLICA_SET_HOSTS']):
                log.msg(
                    'DeprecationWarning: MONGODB_REPLICA_SET_HOSTS is deprecated',
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://%s' % (
                    settings['MONGODB_REPLICA_SET_HOSTS'])

        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('fsync', 'MONGODB_FSYNC'),
            ('write_concern', 'MONGODB_REPLICA_SET_W'),
            ('database', 'MONGODB_DATABASE'),
            ('collection', 'MONGODB_COLLECTION'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
        ]

        for key, setting in options:
            if not not_set(settings[setting]):
                self.config[key] = settings[setting]

    def process_item(self, item, spider):
        """ Process the item and add it to MongoDB

        Args:
            item (str)::
                The item to put into MongoDB
            spider (str)::
                The spider running the queries
        """
        if self.config['unique_key'] is None:
            self.collection.insert(dict(item))
        else:
            self.collection.update(
                {
                    self.config['unique_key']: item[self.config['unique_key']]
                },
                dict(item),
                upsert=True)
        log.msg(
            'Stored item in MongoDB %s/%s' % (
                self.config['database'], self.config['collection']),
            level=log.DEBUG, spider=spider)
        return item