#!/usr/bin/env python3

from tests import codeTester
import unittest
from boil import *
            

class TestBoil(unittest.TestCase):
    def runCodeTest(self, tester, test_language=True, test_extension=True):
        if test_language:
            with self.subTest('basic {0} language'.format(tester.lang)):
                self.assertEqual(
                    Boiler().plate(lang=tester.lang),
                    tester.default)

            with self.subTest('advanced {0} language'.format(tester.lang)):
                self.assertEqual(
                    Boiler().plate(lang=tester.lang, **codeTester.options),
                    tester.advanced)

        if test_extension:
            with self.subTest('basic {0} extension'.format(tester.ext)):
                self.assertEqual(
                    Boiler().plate(ext=tester.ext),
                    tester.default)

            with self.subTest('advanced {0} extension'.format(tester.ext)):
                self.assertEqual(
                    Boiler().plate(ext=tester.ext, **codeTester.options),
                    tester.advanced)

    def test_c(self):
        self.runCodeTest(codeTester.c)

    def test_cpp(self):
        self.runCodeTest(codeTester.cpp)

    def test_java(self):
        self.runCodeTest(codeTester.java)

    def test_python(self):
        self.runCodeTest(codeTester.python)

    def test_python2(self):
        self.runCodeTest(codeTester.python2, test_extension=False)

    def test_python3(self):
        self.runCodeTest(codeTester.python3, test_extension=False)

if __name__ == '__main__':
    unittest.main()
