# grits-net-consume
A Python script to parse the transport network information in the provided format and load it into
MongoDB with geospatial indexing.

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
  ``` python grits_consume.py test/data/Schedule_Weekly_Extract_Report.tsv ```
