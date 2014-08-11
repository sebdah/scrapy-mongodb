"""
Setup script for PyPi
"""

from distutils.core import setup
setup(
    name='scrapy-mongodb',
    version='0.7.2',
    license='Apache License, Version 2.0',
    description='Pipeline to MongoDB for Scrapy. Supports MongoDB replica sets',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='http://sebdah.github.com/scrapy-mongodb/',
    keywords="scrapy mongodb",
    py_modules=['scrapy_mongodb'],
    platforms=['Any'],
    install_requires=[
        'pymongo >= 2.4.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
