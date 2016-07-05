#!/usr/bin/env python3

'''Unit tests for boil.py'''

import unittest
from tests import codetester
import boil


class TestBoil(unittest.TestCase):
    '''Basic boil tests'''

    def run_code_test(self, tester, use_language=True, use_extension=True):
        '''Tests basic & advanced boilerplate by name and extension.'''

        boiler = boil.Boiler()

        if use_language:
            with self.subTest('base {0} from language'.format(tester['lang'])):
                self.assertEqual(
                    boiler.plate(lang=tester['lang']),
                    tester['default'])

            with self.subTest('advanced {0} from language'.format(tester['lang'])):
                self.assertEqual(
                    boiler.plate(lang=tester['lang'], options=codetester.OPTIONS),
                    tester['advanced'])

        if use_extension:
            with self.subTest('base {0} from extension'.format(tester['ext'])):
                self.assertEqual(
                    boiler.plate(ext=tester['ext']),
                    tester['default'])

            with self.subTest('advanced {0} from extension'.format(tester['ext'])):
                self.assertEqual(
                    boiler.plate(ext=tester['ext'], options=codetester.OPTIONS),
                    tester['advanced'])

    def test_code(self):
        '''Runs tests for each language'''

        with self.subTest('c'):
            self.run_code_test(codetester.LANG['c'])

        with self.subTest('cpp'):
            self.run_code_test(codetester.LANG['cpp'])

        with self.subTest('java'):
            self.run_code_test(codetester.LANG['java'])

        with self.subTest('python'):
            self.run_code_test(codetester.LANG['python'])

        with self.subTest('python2'):
            self.run_code_test(codetester.LANG['python2'], use_extension=False)

        with self.subTest('python3'):
            self.run_code_test(codetester.LANG['python3'], use_extension=False)

    def test_lookup_error(self):
        '''Tests for appropriate lookup errors'''

        boiler = boil.Boiler()

        with self.subTest('missing data'):
            self.assertRaises(LookupError, boiler.plate)

        with self.subTest('bad ext data'):
            self.assertRaises(LookupError, boiler.plate, ext='asdf')

        with self.subTest('bad lang data'):
            self.assertRaises(LookupError, boiler.plate, lang='asdf')

if __name__ == '__main__':
    unittest.main()
