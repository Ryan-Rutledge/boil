#!/usr/bin/env python3

import os
import sys
import argparse
from inspect import getsourcefile
sys.path.append(os.path.dirname(__file__))
import boiler


templateDirectory = 'plates'

def getTemplatePath():
    '''Returns path to boilerplate code templates.'''

    # Get path of current code
    source_file = os.path.abspath(getsourcefile(lambda:None))

    # Get directory of current code
    source_dir = os.path.split(source_file)[0]

    # Get directory of boilerplate templates
    return os.path.join(source_dir, templateDirectory)

def parse():
    # Main parser
    parser = argparse.ArgumentParser(prog='boiler', description='Boilerplate code generator.')
    parser.add_argument('-l', '--lang', '--language', help='explicitly name a language to use (default: searches for a file extension match)')

    # Generation parser
    options = parser.add_argument_group('code options')
    options.add_argument('-f', '--func', '--function', action='append', default=[], help='generate empty function out of provided name (can be used multiple times)')
    #options.add_argument('-t', '--tabs', '--tabwidth', type=int, help='expand tabs into a specific number of space characters (default: use tab characters)')

    # Output parser
    output = parser.add_argument_group('output options')
    output.add_argument('-x', '--exec', '--executable', action='store_true', help='attempts to make the file executable with chmod +x')
    output.add_argument('file', nargs='?', help='boilerplate file to be created (default: print to stdout)')

    return vars(parser.parse_args())

def main():
    parser = parse()

    if parser.get('help'):
        parser.print_help()
    else:
        boiler.loadTemplates(getTemplatePath())

        filename = parser.get('file')
        text = boiler.plate(filename, parser)

        if filename:
            # Write output to file
            textfile = open(filename, 'x')
            print(text, end='', file=textfile)
            textfile.close()
        else:
            print(text)

if __name__ == '__main__':
    main()
