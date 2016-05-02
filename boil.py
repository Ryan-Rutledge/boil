#!/usr/bin/env python3

import os
import sys
import stat
import argparse
from boiler import Boiler


def parse(epilog):
    '''Parses command line arguments'''

    # Main parser
    parser = argparse.ArgumentParser(
            description='Simple boilerplate code generator.',
            epilog=epilog)

    parser.add_argument('-l', '--lang', '--language', metavar='LANGUAGE',
        help='Explicitly name a language to use (default: searches for a file'
             ' extension match. If neither a language or a filename with an' \
             ' extension is provided, %(prog)s will exit with error code 1)')

    # Generation parser
    options = parser.add_argument_group('code options')

    options.add_argument('-f', '--force', action='store_true',
        help='Overwrite a file if one already exists' \
             ' (default: %(prog)s will exit with an error code 2)')

    options.add_argument('-m', '--meth', '--method', action='append',
        default=[],
        metavar='METHOD_NAME',
        help='Generates an empty method (can be used multiple times)')

    options.add_argument('-n', '--line', '--newline', action='store_true',
        default=False,
        help='Use a newline after a function declaration' \
             ' (default: single space)')

    options.add_argument('--classname',
        help='Specify a class name for languages that require a boilerplate' \
             ' class (default: uses filename without extension)')

    #options.add_argument('-t', '--tabs', '--tabwidth', type=int,
    #   help='Expand tabs into a specific number of space characters' \
    #        ' (default: use tab characters)')

    # Output parser
    output = parser.add_argument_group('output options')

    output.add_argument('-x', '--exec', '--executable', action='store_true',
        help='Attempts to make the file executable with chmod u+x')
    output.add_argument('file', nargs='?',
        help='Boilerplate file to be created. Returns filename for piping' \
             ' (default: print code to stdout)')

    return vars(parser.parse_args())


def main():
    # Prepare boiler templates
    boiler = Boiler()

    # Format epilog for help page
    def epilog():
        def prettyList(l):
            return ', '.join(list(map(lambda x: "'" + x + "'", l)))

        languages = prettyList(boiler.supportedLanguages())
        extensions = prettyList(boiler.supportedExtensions())

        return 'Supported languages: {0}\n' \
               'Supported extensions: {1}'.format(languages, extensions)

    parser = parse(epilog())

    if parser.get('help'):
        parser.print_help()
    else:
        filepath = parser.get('file')

        name = None
        ext = None

        if filepath:
            filename = os.path.split(filepath)[1]
            name, ext = os.path.splitext(filename)

        if parser.get('classname'):
            name = parser.get('classname')

        # Generate boilerplate code
        text = boiler.plate(ext=ext,
                lang=parser.get('lang'),
                funcs=parser.get('meth'),
                name=name,
                newlines=parser.get('line'))

        if filepath:
            textfile = None

            # Write output to file
            if parser.get('force'):
                textfile = open(filepath, 'w')
            else:
                try:
                    textfile = open(filepath, 'x')
                except FileExistsError:
                    sys.stderr.write(
                        'File cannot be written because it already exists.' \
                        ' Use -f to overwrite.\n')
                    sys.exit(2)

            print(text, end='', file=textfile)
            textfile.close()

            # Make file executable for user
            if parser.get('exec'):
                file_stats = os.stat(filepath).st_mode
                st_mode = stat.S_IMODE(file_stats)
                os.chmod(filepath, st_mode | stat.S_IXUSR)

            print(filepath)
        else:
            print(text, end='')


if __name__ == '__main__':
    main()
