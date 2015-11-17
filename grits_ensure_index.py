#!/usr/bin/env python
import os
import sys
import glob

from conf import settings
from tools.grits_ensure_indexes import GritsEnsureIndexes


""" wrapper for running GritsEnsureIndexes """
if __name__ == '__main__':
    
    cmd = GritsEnsureIndexes()
    cmd.run()