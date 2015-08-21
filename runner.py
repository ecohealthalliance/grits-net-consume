import unittest

import tests.suites.program

test_modules = [tests.suites.program]

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for module in test_modules:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    runner = unittest.TextTestRunner()
    runner.run(suite)