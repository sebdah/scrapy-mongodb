<a href='https://travis-ci.org/sebdah/scrapy-mongodb'><img src='https://secure.travis-ci.org/sebdah/scrapy-mongodb.png?branch=master'></a>

scrapy-mongodb
==============
MongoDB pipeline for Scrapy. This module supports both MongoDB in standalone setups and replica sets. This module will insert the items to MongoDB as soon as your spider finds data to extract.

`scrapy-mongodb` can also buffer objects if you prefer to write chunks of data to MongoDB rather than one write per document. See the `MONGODB_BUFFER_DATA` option for details.

Installation
------------
Install via `pip`:

    pip install scrapy-mongodb

Configuration
-------------

### Basic configuration example
Add `scrapy-mongodb` to your projects `settings.py` file.

    ITEM_PIPELINES = [
      'scrapy_mongodb.MongoDBPipeline',
    ]

    MONGODB_URI = 'mongodb://localhost:27017'
    MONGODB_DATABASE = 'scrapy'
    MONGODB_COLLECTION = 'my_items'

If you want a unique key in your database, add the key to the configuration like this:

    MONGODB_UNIQUE_KEY = 'url'

### Configure MongoDB replica sets

You can configure `scrapy-mongodb` to support MongoDB replica sets simply by adding the `MONGODB_REPLICA_SET` and `MONGODB_REPLICA_SET_HOSTS` config option:

    MONGODB_REPLICA_SET = 'myReplicaSetName'
    MONGODB_URI = 'mongodb://host1.example.com:27017,host2.example.com:27017,host3.example.com:27017'

If you need to ensure that your data has been replicated, use the `MONGODB_REPLICA_SET_W` option. It is an implementation of the `w` parameter in `pymongo`. Details from the `pymongo` documentation:

    Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.

### Configure data buffering

To ease the load on MongoDB `scrapy-mongodb` has a buffering feature. You can enable it by simply setting the `MONGODB_BUFFER_DATA` to the buffer size you want. If you set it to `10` `scrapy-mongodb` will write 10 documents at a time to MongoDB.

    MONGODB_BUFFER_DATA = 10

It is not possible to combine this feature with `MONGODB_UNIQUE_KEY`. Technically due to that the `update` method in `pymongo` doesn't support multi doc updates.

### Adding timestamps

`scrapy-mongodb` can append a timestamp to your item when inserting it to the database. Enable this feature by like this:

    MONGODB_ADD_TIMESTAMP = True

This will modify the document to look something like this:

    {
        ...
        'scrapy-mongodb': {
            'ts': ISODate("2013-01-10T07:43:56.797Z")
        }
        ...
    }

The timestamp is in UTC.

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
        <td>scrapy-mongodb</td>
        <td>No</td>
        <td>Database name to use. Does not need to exist.</td>
    </tr>
    <tr>
        <td>MONGODB_COLLECTION</td>
        <td>items</td>
        <td>No</td>
        <td>Collection within the database to use. Does not need to exist.</td>
    </tr>
    <tr>
        <td>MONGODB_URI</td>
        <td>mongodb://localhost:27017</td>
        <td>No</td>
        <td>
            Add the URI to the MongoDB instance or replica set you want to connect to. It must start with mongodb://. See more in the MongoDB docs 1). Some example strings:<br />
            mongodb://user:pass@host:port<br />
            mongodb://user:pass@host:port,host2:port2,
        </td>
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
        <td>MONGODB_BUFFER_DATA</td>
        <td>None</td>
        <td>No</td>
        <td>
            To ease the load on MongoDB you might want to buffer data in the client before sending it to MongoDB. Set this option to the number of items you want to buffer in the client before sending them to MongoDB. Setting a MONGODB_UNIQUE_KEY together with MONGODB_BUFFER_DATA is not supported.
        </td>
    </tr>
    <tr>
        <td>MONGODB_ADD_TIMESTAMP</td>
        <td>False</td>
        <td>No</td>
        <td>
            If this is set to True, scrapy-mongodb will add a timestamp key to the documents. The document will look like this:<br />
            { scrapy_mongo: { ts: ISODate("2013-01-10T07:43:56.797Z") } }
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
        <td>MONGODB_REPLICA_SET_W</td>
        <td>0</td>
        <td>No</td>
        <td>
            Best described in the pymongo documentation 2):<br/>
            Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.
        </td>
    </tr>
    <tr>
        <td>MONGODB_STOP_ON_DUPLICATE</td>
        <td>0</td>
        <td>No</td>
        <td>
            Set this to a value greater than zero to close the spider when a specific number of duplicated insertions in mongodb are detected.<br/>
            If set to zero, this option has no effect.<br/>
            If set to something greater than zero, say N, the spider is closed when N duplicated insertions are detected during the crawling.
        </td>
    </tr>
</table>

1. [http://docs.mongodb.org/manual/reference/connection-string/](http://docs.mongodb.org/manual/reference/connection-string/)
2. [http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient](http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient)

### Deprecated config options

<table border='1'>
    <tr>
        <td>MONGODB_HOST</td>
        <td>localhost</td>
        <td>No</td>
        <td>
            DEPRECATED since scrapy-mongodb 0.5.0, use MONGODB_URI instead.<br />
            MongoDB host name to connect to.
        </td>
    </tr>
    <tr>
        <td>MONGODB_PORT</td>
        <td>27017</td>
        <td>No</td>
        <td>
            DEPRECATED since scrapy-mongodb 0.5.0, use MONGODB_URI instead.<br />
            MongoDB port number to connect to.
        </td>
    </tr>
    <tr>
        <td>MONGODB_REPLICA_SET_HOSTS</td>
        <td>None</td>
        <td>No</td>
        <td>
            DEPRECATED since scrapy-mongodb 0.5.0, use MONGODB_URI instead.<br />
            Host string to use to connect to the replica set. See the hosts_or_uri option in the pymongo documentation.
        </td>
    </tr>
</table>

Release information
-------------------
**0.7.2 (2014-08-11)**
- [#18 Enable multiple value index for collection](https://github.com/sebdah/scrapy-mongodb/pull/18). Thanks [@sherzberg](https://github.com/sherzberg) for the pull request

**0.7.1 (2014-04-14)**
- Fixed bad log messages when duplicate keys were found

**0.7.0 (2014-04-07)**
- [#13 Add option to allow closing the spider upon duplicate insertion in mongodb](https://github.com/sebdah/scrapy-mongodb/pull/13)

**0.6.4 (2014-04-07)**
- Add the MONGODB_STOP_ON_DUPLICATE option which allows to close the spider when a certain amount of duplicated insertion threshold is reached.

**0.6.3 (2014-03-24)**
- Syncing all items not previously synced from the local buffer to MongoDB when the spider finishes

**0.6.2 (2013-08-23)**
- [#10 get_project_settings precludes configuring settings on command line](https://github.com/sebdah/scrapy-mongodb/pull/10)

**0.6.1 (2013-07-14)**
- [#9 fix: item_buffer.append() takes exactly one argument (0 given)](https://github.com/sebdah/scrapy-mongodb/pull/9)

**0.6.0 (2013-06-04)**
- [#6 ScrapyDeprecationWarning: crawler.settings](https://github.com/sebdah/scrapy-mongodb/issues/6)
- [#7 Use Python format() for output](https://github.com/sebdah/scrapy-mongodb/issues/7)
- [#8 Bug when upserting items with a unique key](https://github.com/sebdah/scrapy-mongodb/issues/8)

**0.5.1 (2013-06-03)**
- Updated docstrings

**0.5.0 (2013-01-10)**
- Implemented feature [#5 Add flag for setting timestamps in the database](https://github.com/sebdah/scrapy-mongodb/issues/5)
- Implemented feature [#4 Implement support for MongoDB authentication](https://github.com/sebdah/scrapy-mongodb/issues/4)
- Implemented feature [#3 Add support for MongoDB URIs when connecting](https://github.com/sebdah/scrapy-mongodb/issues/3)
- Implemented feature [#2 Support buffered data](https://github.com/sebdah/scrapy-mongodb/issues/2)

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

    make release

Author
------

This project is maintained by [Sebastian Dahlgren](http://www.sebastiandahlgren.se) ([GitHub](https://github.com/sebdah) | [Twitter](https://twitter.com/sebdah) | [LinkedIn](http://www.linkedin.com/in/sebastiandahlgren))

License
-------

APACHE LICENSE 2.0
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
