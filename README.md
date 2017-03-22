# grits-net-consume
[![Build Status](https://circleci.com/gh/ecohealthalliance/grits-net-consume.svg?style=shield&circle-token=6ec5b4f6d79595bb412aaa793c61c3d01c4f87e3)](https://circleci.com/gh/ecohealthalliance/grits-net-consume)

A Python script to parse the transport network information in the provided format and load it into
MongoDB with geospatial indexing.

## Prerequisites

##### Mac OS X
  - Xcode
  - homebrew
  - python (2.7.10)
See the following guide: http://docs.python-guide.org/en/latest/starting/install/osx/

##### Ubuntu
 - build-essential (provides gcc)
 - python (2.7.10)
 - python-dev (2.7.10)
 - python-setuptools

## Install

1. setup virtualenv

  ``` virtualenv grits-net-consume-env```

2. activate the virtual environment

  ``` source grits-net-consume-env/bin/activate```

3. install 3rd party libraries

  ``` pip install -r requirements.txt```

## User Defined Settings

### Environment variables
Environment variables may be used for [MONGO_HOST, MONGO_DATABASE, MONGO_USERNAME, MONGO_PASSWORD].
Note:  these will override any value set within settings.py but not arguments to the program

Ex: `~/git/grits-net-consume$ MONGO_HOST='10.0.1.2' python grits_consume.py` 

### settings.py

User defined settings may be set within `conf/settings.py`, which include:

  ```
  _DEBUG #boolean, true enables logging.debug messages
  _DATA_DIR #string, location of the FTP downloaded files ex '/data/'
  _ALLOWED_FILE_EXTENSIONS #array, allowed extensions for data files ex. ['.tsv','.csv']
  _TYPES = #array, types of data files ex. ['DiioAirport', 'FlightGlobal', 'FixAirports']
  _STRFTIME_FORMAT #string, default strftime format for a records date field ex. '%b %Y'
  _AIRPORT_COLLECTION_NAME #string, mongodb collection names ex. 'airports'
  _FLIGHT_COLLECTION_NAME #string, mongodb collection names ex. 'flights'
  _INVALID_RECORD_COLLECTION_NAME #string, mongodb collection names ex. 'invalidRecords'
  _DISABLE_SCHEMA_MATCH #boolean, raise exception for headers not in the schema?
  _CHUNK_SIZE #integer, number of lines to split the input file
  _NODES #integer, number of threads to launch
  _THREADING_ENABLED #boolean, true enables multi-threading
  _MONGO_HOST #string, default command-line option for when -m is not specified ex. 'localhost'
  _MONGO_DATABASE #string, default command-line option for when -d is not specified ex. 'grits'
  _MONGO_USERNAME #string or None, default command-line option for when -u is not specified ex. None
  # Warning: this will be stored in plain-text
  _MONGO_PASSWORD #string or None, default command-line option for when -p is not specified ex. None
  ```

## Test
  ``` nosetests ```

## Run

1. Upsert airport data (NOTE: This would be done a periodic basis, such as once
   a month.  However, it must be done at least once prior to running the flight
   data import below.)

  ```
  python grits_consume.py --type DiioAirport tests/data/MiExpressAllAirportCodes.tsv
  ```

2. Upsert flight extraction report data

  2a.  Example of upserting test data:
  ``` 
  python grits_consume.py --type FlightGlobal tests/data/GlobalDirectsSample_20150728.csv
  ```
  
  2b.  Example of upserting last FTP data (no args):
  ``` 
  python grits_consume.py
  ```

3. Create the indexes on the database
  ``` 
  python grits_ensure_index.py
  ```
##### Fixing airport locations
Some airports are imported with the incorrect location information.  The current `DiioAirport` import will fix airports with incorrect locations autoamtically, but existing airport collections can be fixed by running:
```
python grits_consume.py --type FixAirports tests/data/errorports.csv
```


## Program Options

  ```
  usage: grits_consume.py [-h] [-v] -t {DiioAirport,FlightGlobal} [-u USERNAME]
                        [-p PASSWORD] [-d DATABASE] [-m MONGOHOST]
                        infile

  script to parse the grits transportation network data file and populate a
  mongodb collection.

  positional arguments:
    infile                the file to be parsed

  optional arguments:
    -h, --help            show this help message and exit
    -v, --verbose         verbose output
    -t {DiioAirport,FlightGlobal,FixAirports}, --type {DiioAirport,FlightGlobal,FixAirports}
                          the type of report to be parsed
    -u USERNAME, --username USERNAME
                          the username for mongoDB (Default: None)
    -p PASSWORD, --password PASSWORD
                          the password for mongoDB (Default: None)
    -d DATABASE, --database DATABASE
                          the database for mongoDB (Default: grits)
    -m MONGOHOST, --mongohost MONGOHOST
                          the hostname for mongoDB (Default: localhost)
  ```
  
  ```
  usage: grits_ensure_index.py [-h] [-u USERNAME] [-p PASSWORD] [-d DATABASE]
                               [-m MONGOHOST]
  
  script to set the mongodb indexes for grits transportation network data.
  
  optional arguments:
    -h, --help            show this help message and exit
    -u USERNAME, --username USERNAME
                          the username for mongoDB (Default: None)
    -p PASSWORD, --password PASSWORD
                          the password for mongoDB (Default: None)
    -d DATABASE, --database DATABASE
                          the database for mongoDB (Default: grits)
    -m MONGOHOST, --mongohost MONGOHOST
                          the hostname for mongoDB (Default: localhost)

  ```


## License
Copyright 2016 EcoHealth Alliance

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
