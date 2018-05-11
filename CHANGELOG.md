# CHANGELOG

## 0.12.0 (2018-01-08)
- Add Python 3 support [#42](https://github.com/sebdah/scrapy-mongodb/issues/42)

## 0.11.0 (2017-08-09)
- Do not store `None` or empty value objects in MongoDB [#39](https://github.com/sebdah/scrapy-mongodb/issues/39)
- Fix memory leak [#38](https://github.com/sebdah/scrapy-mongodb/issues/38)
- Fix bug in logging [#40](https://github.com/sebdah/scrapy-mongodb/issues/40)

## 0.10.0 (2017-08-03)
- Store items from different spiders in different collections [#36](https://github.com/sebdah/scrapy-mongodb/pull/36)
- Fix a number of deprecation warnings [#34](https://github.com/sebdah/scrapy-mongodb/issues/34)
- Update `scrapy` version to 1.4.0

## 0.9.1 (2015-12-18)
- Fix typo

## 0.9.0 (2015-04-10)
- [#28 Allow per-spider configuration](https://github.com/sebdah/scrapy-mongodb/pull/28). Thanks [@thiagof](https://github.com/thiagof) for the pull request

## 0.8.2 (2015-03-11)
- [#26 Unicode log message](https://github.com/sebdah/scrapy-mongodb/issue/26). Thanks [@italomaia](https://github.com/italomaia) for the pull request

## 0.8.1 (2015-03-05)
- [#25 Add unicode shebang](https://github.com/sebdah/scrapy-mongodb/pull/25). Thanks [@italomaia](https://github.com/italomaia) for the pull request

## 0.8.0 (2014-12-25)
- [#22 Call serializer before inserting](https://github.com/sebdah/scrapy-mongodb/issue/22). Thanks [@italomaia](https://github.com/italomaia) for the pull request

## 0.7.2 (2014-08-11)
- [#18 Enable multiple value index for collection](https://github.com/sebdah/scrapy-mongodb/pull/18). Thanks [@sherzberg](https://github.com/sherzberg) for the pull request

## 0.7.1 (2014-04-14)
- Fixed bad log messages when duplicate keys were found

## 0.7.0 (2014-04-07)
- [#13 Add option to allow closing the spider upon duplicate insertion in mongodb](https://github.com/sebdah/scrapy-mongodb/pull/13)

## 0.6.4 (2014-04-07)
- Add the MONGODB_STOP_ON_DUPLICATE option which allows to close the spider when a certain amount of duplicated insertion threshold is reached.

## 0.6.3 (2014-03-24)
- Syncing all items not previously synced from the local buffer to MongoDB when the spider finishes

## 0.6.2 (2013-08-23)
- [#10 get_project_settings precludes configuring settings on command line](https://github.com/sebdah/scrapy-mongodb/pull/10)

## 0.6.1 (2013-07-14)
- [#9 fix: item_buffer.append() takes exactly one argument (0 given)](https://github.com/sebdah/scrapy-mongodb/pull/9)

## 0.6.0 (2013-06-04)
- [#6 ScrapyDeprecationWarning: crawler.settings](https://github.com/sebdah/scrapy-mongodb/issues/6)
- [#7 Use Python format() for output](https://github.com/sebdah/scrapy-mongodb/issues/7)
- [#8 Bug when upserting items with a unique key](https://github.com/sebdah/scrapy-mongodb/issues/8)

## 0.5.1 (2013-06-03)
- Updated docstrings

## 0.5.0 (2013-01-10)
- Implemented feature [#5 Add flag for setting timestamps in the database](https://github.com/sebdah/scrapy-mongodb/issues/5)
- Implemented feature [#4 Implement support for MongoDB authentication](https://github.com/sebdah/scrapy-mongodb/issues/4)
- Implemented feature [#3 Add support for MongoDB URIs when connecting](https://github.com/sebdah/scrapy-mongodb/issues/3)
- Implemented feature [#2 Support buffered data](https://github.com/sebdah/scrapy-mongodb/issues/2)

## 0.4.0 (2013-01-07)
- Added support for MongoDB replica set host strings

## 0.3.0 (2013-01-06)
- Minor supportive updates

## 0.2.0 (2013-01-06)
- Fixed connection problem for MongoDB replica sets
- Fixed bad default parameter handling

## 0.1.0 (2013-01-06)
- Initial release of the `scrapy-mongodb` pipeline module
- Support for MongoDB replica sets and standalone databases
