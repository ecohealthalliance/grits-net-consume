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

1. Upsert airport data
  ``` python grits_consume.py --type airport test/data/MiExpressAllAirportCodes.tsv ```

2. Upsert extration report data
  ``` python grits_consume.py --type extract test/data/Schedule_Weekly_Extract_Report.tsv ```