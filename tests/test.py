#!/usr/bin/env python3

from tests import codeTester
import unittest
from boil import *
            

class TestBoil(unittest.TestCase):
    def runCodeTest(self, tester, use_language=True, use_extension=True):
        boiler = Boiler()

        if use_language:
            with self.subTest('base {0} from language'.format(tester.lang)):
                self.assertEqual(
                    boiler.plate(lang=tester.lang),
                    tester.default)

            with self.subTest('advanced {0} from language'.format(tester.lang)):
                self.assertEqual(
                    boiler.plate(lang=tester.lang, **codeTester.options),
                    tester.advanced)

        if use_extension:
            with self.subTest('base {0} from extension'.format(tester.ext)):
                self.assertEqual(
                    boiler.plate(ext=tester.ext),
                    tester.default)

            with self.subTest('advanced {0} from extension'.format(tester.ext)):
                self.assertEqual(
                    boiler.plate(ext=tester.ext, **codeTester.options),
                    tester.advanced)

    def test_code(self):
        with self.subTest('c'):
            self.runCodeTest(codeTester.c)

        with self.subTest('cpp'):
            self.runCodeTest(codeTester.cpp)

        with self.subTest('java'):
            self.runCodeTest(codeTester.java)

        with self.subTest('python'):
            self.runCodeTest(codeTester.python)

        with self.subTest('python2'):
            self.runCodeTest(codeTester.python2, use_extension=False)

        with self.subTest('python3'):
            self.runCodeTest(codeTester.python3, use_extension=False)

    def test_lookup_error(self):
        boiler = Boiler()

        with self.subTest('missing data'):
            self.assertRaises(LookupError, boiler.plate)

        with self.subTest('bad ext data'):
            self.assertRaises(LookupError, boiler.plate, ext='asdf')

        with self.subTest('bad lang data'):
            self.assertRaises(LookupError, boiler.plate, lang='asdf')

if __name__ == '__main__':
    unittest.main()
