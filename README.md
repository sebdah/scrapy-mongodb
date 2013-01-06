scrapy-mongodb
==============
MongoDB pipeline for Scrapy. This module supports both MongoDB in standalone setups and replica sets. This module will insert the items to MongoDB as soon as your spider finds data to extract.

Installation
------------
Install via `pip`:

    pip install scrapy-mongodb

Basic configuration
-------------------
Add `scrapy-mongodb` to your projects `settings.py` file.

    ITEM_PIPELINES = [
      'scrapy_mongodb.MongoDBPipeline',
    ]

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DATABASE = 'scrapy'
    MONGODB_COLLECTION = 'my_items'

If you want a unique key in your database, add the key to the configuration like this:

    MONGODB_UNIQUE_KEY = 'url'

Configure MongoDB replica sets
------------------------------
You can configure `scrapy-mongodb` to support MongoDB replica sets simply by adding the `MONGODB_REPLICA_SET` config option:

    MONGODB_REPLICA_SET = 'myReplicaSetName'

If you need to ensure that your data has been replicated, use the `` option. It is an implementation of the `w` parameter in `pymongo`. Details from the `pymongo` documentation:

"""
Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.
"""

Full list of config options
---------------------------
**MONGODB_HOST** (default: 'localhost')
MongoDB host name to connect to

**MONGODB_PORT** (default: 27017)
MongoDB port number to connect to

**MONGODB_DATABASE** (required)
Database name to use. Does not need to exist.

**MONGODB_COLLECTION** (required)
Collection within the database to use. Does not need to exist.

**MONGODB_UNIQUE_KEY** (default: None)
If you want to have a unique key in the database, enter the key name here. `scrapy-mongodb` will ensure the key is properly indexed.

**MONGODB_FSYNC** (default: False)
If this is set to `True` it forces MongoDB to wait for all files to be synced before returning.

**MONGODB_REPLICA_SET** (default: None)
Set this if you want to enable replica set support. The option should be given the name of the replica set you want to connect to. `MONGODB_HOST` and `MONGODB_PORT` should point at your config server.

**MONGODB_REPLICA_SET_W** (default: 0)
Best described in the [pymongo documentation](http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient):
Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.

Release information
-------------------
**0.2.0 (2013-01-06)**
- Fixed connection problem for MongoDB replica sets
- Fixed bad default parameter handling

**0.1.0 (2013-01-06)**
- Initial release of the `scrapy-mongodb` pipeline module
- Support for MongoDB replica sets and standalone databases

Instructions to release project to PyPi
---------------------------------------

    python setup.py register
    python setup.py sdist upload
