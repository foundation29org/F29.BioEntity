import unittest

from BioEntityTests import *

USE_CACHE = True

suite = unittest.TestSuite()

suite.addTest(HPOGraphTests('en', use_cache=USE_CACHE))
suite.addTest(MondoGraphTests('en', use_cache=USE_CACHE))
suite.addTest(BioPhensTests('en', use_cache=USE_CACHE))

suite.addTest(BioGenesTests(use_cache=USE_CACHE))

suite.addTest(HPOGraphTests('es', use_cache=USE_CACHE))
suite.addTest(MondoGraphTests('es', use_cache=USE_CACHE))
suite.addTest(BioPhensTests('es', use_cache=USE_CACHE))

unittest.TextTestRunner(verbosity=2).run(suite)

