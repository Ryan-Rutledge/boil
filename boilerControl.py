#!/usr/bin/env python3

import os
import sys
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

def write(text, filename):
    '''Copies text into a new file.'''

    textfile = open(filename, 'x')
    print(tempfile.read(), end='', file=textfile)
    
    textfile.close()

def main():
    # TODO: when creating boilerplate, check for --create and --editor flags
    boiler.loadTemplates(getTemplatePath())
    boiler.plate('tmp.py')

if __name__ == '__main__':
    main()
