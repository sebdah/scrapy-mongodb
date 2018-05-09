[![PyPI version](https://badge.fury.io/py/scrapy-mongodb.svg)](https://badge.fury.io/py/scrapy-mongodb)
[![Build Status](https://travis-ci.org/sebdah/scrapy-mongodb.svg?branch=master)](https://travis-ci.org/sebdah/scrapy-mongodb)

# scrapy-mongodb
MongoDB pipeline for Scrapy. This module supports both MongoDB in standalone setups and replica sets. This module will insert the items to MongoDB as soon as your spider finds data to extract.

`scrapy-mongodb` can also buffer objects if you prefer to write chunks of data to MongoDB rather than one write per document. See the `MONGODB_BUFFER_DATA` option for details.

## INSTALLATION
Install via `pip`:
```
pip install scrapy-mongodb
```

## CONFIGURATION
### Basic configuration
Add `scrapy-mongodb` to your projects `settings.py` file.
```
ITEM_PIPELINES = [
  'scrapy_mongodb.MongoDBPipeline',
]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'my_items'
```

If you want a unique key in your database, add the key to the configuration like this:
```
MONGODB_UNIQUE_KEY = 'url'
```

### MongoDB replica sets
You can configure `scrapy-mongodb` to support MongoDB replica sets simply by adding the `MONGODB_REPLICA_SET` and `MONGODB_REPLICA_SET_HOSTS` config option:
```
MONGODB_REPLICA_SET = 'myReplicaSetName'
MONGODB_URI = 'mongodb://host1.example.com:27017,host2.example.com:27017,host3.example.com:27017'
```

If you need to ensure that your data has been replicated, use the `MONGODB_REPLICA_SET_W` option. It is an implementation of the `w` parameter in `pymongo`. Details from the `pymongo` documentation:
```
Write operations will block until they have been replicated to the specified number or tagged set of servers. w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries). Passing w=0 disables write acknowledgement and all other write concern options.
```

### Data buffering
To ease the load on MongoDB `scrapy-mongodb` has a buffering feature. You can enable it by simply setting the `MONGODB_BUFFER_DATA` to the buffer size you want. If you set it to `10` `scrapy-mongodb` will write 10 documents at a time to MongoDB.
```
MONGODB_BUFFER_DATA = 10
```

It is not possible to combine this feature with `MONGODB_UNIQUE_KEY`. Technically due to that the `update` method in `pymongo` doesn't support multi doc updates.

### Adding timestamps
`scrapy-mongodb` can append a timestamp to your item when inserting it to the database. Enable this feature by like this:
```
MONGODB_ADD_TIMESTAMP = True
```

This will modify the document to look something like this:
```
{
    ...
    'scrapy-mongodb': {
        'ts': ISODate("2013-01-10T07:43:56.797Z")
    }
    ...
}
```

*The timestamp is in UTC.*

### Write to one collection per spider
It's possible to write data to one collection per spider. To enable that
feature, set this environment variable.
```
MONGODB_SEPARATE_COLLECTIONS = True
```

### Full list of config options
Configuration options available. Put these in your `settings.py` file.

| **Parameter** | **Default** | **Required?** | **Description** |
| --- | --- | --- | --- |
| MONGODB_DATABASE | scrapy-mongodb | No | Database to use. Does not need to exist. |
| MONGODB_COLLECTION | items | No | Collection within the database to use. Does not need to exist. |
| MONGODB_URI | mongodb://localhost:27017 | No | URI to the MongoDB instance or replica set you want to connect to. It must start with `mongodb://` (see more in the [MongoDB docs][1]). E.g.: `mongodb://user:pass@host:port`, `mongodb://user:pass@host:port,host2:port2` |
| MONGODB_UNIQUE_KEY | None | No | If you want to have a unique key in the database, enter the key name here. scrapy-mongodb will ensure the key is properly indexed. |
| MONGODB_BUFFER_DATA | None | No | To ease the load on MongoDB, set this option to the number of items you want to buffer in the client before sending them to database. Setting a MONGODB_UNIQUE_KEY together with MONGODB_BUFFER_DATA is not supported. |
| MONGODB_ADD_TIMESTAMP | False | No | If set to True, scrapy-mongodb will add a timestamp key to the documents. The document will look like this: `{scrapy_mongo: {ts: ISODate("2013-01-10T07:43:56.797Z")}}`
| MONGODB_FSYNC | False | No | If set to True, it forces MongoDB to wait for all files to be synced before returning. |
| MONGODB_REPLICA_SET | None | Yes, for replica sets | Set this if you want to enable replica set support. The option should be given the name of the replica set you want to connect to. MONGODB_URI should point at your config server. |
| MONGODB_REPLICA_SET_W | 0 | No | Best described in the [pymongo docs][2]. Write operations will block until they have been replicated to the specified number or tagged set of servers, including the replica set primary. E.g.: `w=3` means write to the primary and wait until replicated to 2 secondaries. Passing `w=0` disables write acknowledgement and all other write concern options.
| MONGODB_STOP_ON_DUPLICATE | 0 | No | Set this to a value greater than 0 to close the spider when that number of duplicated insertions in MongoDB are detected. If set to 0, this option has no effect. |

[1]: http://docs.mongodb.org/manual/reference/connection-string
[2]: http://api.mongodb.org/python/current/api/pymongo/mongo_replica_set_client.html#pymongo.mongo_replica_set_client.MongoReplicaSetClient

### Deprecated config options
*Since scrapy-mongodb 0.5.0*

| **Parameter** | **Default** | **Required?** | **Description** |
| --- | --- | --- | --- |
| MONGODB_HOST | localhost | No | MongoDB host name to connect to. Use MONGODB_URI instead. |
| MONGODB_PORT| 27017 | No | MongoDB port number to connect to. Use MONGODB_URI instead. |
| MONGODB_REPLICA_SET_HOSTS | None | No | Host string to use to connect to the replica set. See the `hosts_or_uri` option in the pymongo docs. Use MONGODB_URI instead. |

## PUBLISHING TO PYPI
```
make release
```

## CHANGELOG
[Read more here](./CHANGELOG.md).

## AUTHOR
This project is maintained by: [Sebastian Dahlgren](http://www.sebastiandahlgren.se) ([GitHub](https://github.com/sebdah) | [Twitter](https://twitter.com/sebdah) | [LinkedIn](http://www.linkedin.com/in/sebastiandahlgren)).

## LICENSE
[Read more here](./LICENSE).
