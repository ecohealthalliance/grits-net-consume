# grits-net-consume
[![Build Status](https://circleci.com/gh/ecohealthalliance/grits-net-consume.svg?style=shield&circle-token=6ec5b4f6d79595bb412aaa793c61c3d01c4f87e3)](https://circleci.com/gh/ecohealthalliance/grits-net-consume)

A Python script to parse the transport network information in the provided format and load it into
MongoDB with geospatial indexing.

## prerequisites

##### Machintosh OS X
  - Xcode
  - homebrew
  - python (2.7.10)
See the following guide: http://docs.python-guide.org/en/latest/starting/install/osx/

##### Ubuntu
 - build-essential (for gcc)
 - python (2.7.10)
 - python-dev (2.7.10)
 - python-setuptools

## install

1. setup virtualenv

  ``` virtualenv grits-net-consume-env```

2. activate the virtual environment

  ``` source grits-net-consume-env/bin/activate```

3. install 3rd party libraries

  ``` pip install -r requirements.txt```

## test
  ``` nosetests ```

## run

1. Upsert airport data (NOTE: This would be done a periodic basis, such as once
   a month.  However, it must be done at least once prior to running the flight
   data import below.)

  ```
  python grits_consume.py --type DiioAirport test/data/MiExpressAllAirportCodes.tsv
  ```

2. Upsert flight extraction report data

  ``` 
  python grits_consume.py --type FlightGlobal test/data/GlobalDirectsSample_20150728.csv
  ```


## program options

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
	  -t {DiioAirport,FlightGlobal}, --type {DiioAirport,FlightGlobal}
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
