#!/usr/bin/env python
import os
import sys
import glob

from conf import settings
from tools.grits_consumer import GritsConsumer


""" wrapper for running GritsConsumer """
if __name__ == '__main__':
    
    cmd = GritsConsumer()
    
    def get_lastest_csv():
        """ get the most recent filename, sorted by date with extension .csv """
        data_dir = os.path.join(os.getcwd() + settings._DATA_DIR)
        return max(glob.iglob(data_dir + '*.[Cc][Ss][Vv]'), key=os.path.getctime)
    
    if len(sys.argv) <= 1:
        lastest_csv = get_lastest_csv()
        cmd.run('--type', 'FlightGlobal', lastest_csv)
    else:
        cmd.run()