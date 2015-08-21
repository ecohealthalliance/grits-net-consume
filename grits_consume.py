#!/usr/bin/env python
import vendor
vendor.add('lib')

from tools.grits_consumers import GritsConsumer

""" wrapper for running GritsConsumer, adds the lib\ directory to PYTHONPATH """

if __name__ == '__main__':
    cmd = GritsConsumer()
    cmd.run()