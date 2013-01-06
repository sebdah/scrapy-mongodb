"""
Setup script for PyPi
"""

from distutils.core import setup
setup(name='scrapy-mongodb',
    version='0.1.0',
    license='Apache License, Version 2.0',
    description='Pipeline to MongoDB for Scrapy. Supports MongoDB replica sets',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='http://github.com/sebdah/scrapy-mongodb',
    keywords="scrapy mongodb",
    py_modules=['scrapy_mongodb'],
    platforms=['Any'],
    install_requires=['pymongo'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)