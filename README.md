<a href='https://travis-ci.org/sebdah/scrapy-mongodb'><img src='https://secure.travis-ci.org/sebdah/scrapy-mongodb.png?branch=master'></a>

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
You can configure `scrapy-mongodb` to support MongoDB replica sets simply by adding the `MONGODB_REPLICA_SET` and `MONGODB_REPLICA_SET_HOSTS` config option:

    MONGODB_REPLICA_SET = 'myReplicaSetName'
    MONGODB_REPLICA_SET_HOSTS = 'host1.example.com:27017,host2.example.com:27017,host3.example.com:27017'

If you need to ensure that your data has been replicated, use the `MONGODB_REPLICA_SET_W` option. It is an implementation of the `w` parameter in `pymongo`. Details from the `pymongo` documentation:

    Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.

Full list of config options
---------------------------
Configuration options available. Put these in your `settings.py` file.

<table border='1'>
    <tr>
        <th>Parameter</th>
        <th>Default</th>
        <th>Required?</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>MONGODB_DATABASE</td>
        <td>None</td>
        <td>Yes</td>
        <td>Database name to use. Does not need to exist.</td>
    </tr>
    <tr>
        <td>MONGODB_COLLECTION</td>
        <td>None</td>
        <td>Yes</td>
        <td>Collection within the database to use. Does not need to exist.</td>
    </tr>
    <tr>
        <td>MONGODB_HOST</td>
        <td>localhost</td>
        <td>No</td>
        <td>MongoDB host name to connect to.</td>
    </tr>
    <tr>
        <td>MONGODB_PORT</td>
        <td>27017</td>
        <td>No</td>
        <td>MongoDB port number to connect to.</td>
    </tr>
    <tr>
        <td>MONGODB_UNIQUE_KEY</td>
        <td>None</td>
        <td>No</td>
        <td>
            If you want to have a unique key in the database, enter the key name here. scrapy-mongodb will ensure the key is properly indexed.
        </td>
    </tr>
    <tr>
        <td>MONGODB_FSYNC</td>
        <td>False</td>
        <td>No</td>
        <td>
            If this is set to True it forces MongoDB to wait for all files to be synced before returning.
        </td>
    </tr>
    <tr>
        <td>MONGODB_REPLICA_SET</td>
        <td>None</td>
        <td>Yes, for replica sets</td>
        <td>
            Set this if you want to enable replica set support. The option should be given the name of the replica set you want to connect to. MONGODB_HOST and MONGODB_PORT should point at your config server.
        </td>
    </tr>
    <tr>
        <td>MONGODB_REPLICA_SET_HOSTS</td>
        <td>None</td>
        <td>Yes, for replica sets</td>
        <td>
            Host string to use to connect to the replica set. See the hosts_or_uri option in the pymongo documentation 1).
        </td>
    </tr>
    <tr>
        <td>MONGODB_REPLICA_SET_W</td>
        <td>0</td>
        <td>No</td>
        <td>
            Best described in the pymongo documentation 1):<br/>
            Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.
        </td>
    </tr>
</table>

1. [http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient](http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient)

Release information
-------------------
**0.4.0 (2013-01-07)**
- Added support for MongoDB replica set host strings

**0.3.0 (2013-01-06)**
- Minor supportive updates

**0.2.0 (2013-01-06)**
- Fixed connection problem for MongoDB replica sets
- Fixed bad default parameter handling

**0.1.0 (2013-01-06)**
- Initial release of the `scrapy-mongodb` pipeline module
- Support for MongoDB replica sets and standalone databases

Instructions to release project to PyPi
---------------------------------------

    python setregister
    python setup.py sdist upload
