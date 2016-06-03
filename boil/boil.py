#!/usr/bin/env python3

import re
import os
import sqlite3


class Boiler:
    '''Boilerplate code template manager.'''

    _DEF_PLATE_DIR = 'plates.db'

    _QUERY = {
        'languages':  '''
            SELECT name
            FROM names
            ORDER BY name;''',

        'extensions': '''
            SELECT '.' || extension
            FROM extensions
            ORDER BY extension;''',

        'byEither'  : '''
            SELECT t.template
            FROM templates t, (
                SELECT template_id, 1 AS filter
                FROM names
                WHERE name = ?
                UNION
                SELECT template_id, 2 AS filter
                FROM extensions
                WHERE extension = ?
            ) n
            WHERE t.id = n.template_id
            LIMIT 1;'''
    }

    def __init__(self, template_directory=None):
        self.plates_path = None # Absolute path to boilerplate templates
        self.con = None         # Database connection
        self.cor = None         # Database cursor

        self.loadTemplates(template_directory)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def _getDefaultPlatesPath(self):
        from inspect import getsourcefile

        # Get path of current code
        source_file = os.path.realpath(getsourcefile(lambda:None))

        # Get directory of current code
        source_dir = os.path.split(source_file)[0]

        # Get directory of boilerplate templates
        return os.path.join(source_dir, Boiler._DEF_PLATE_DIR)

    def _getQuery(self, query, *args):
        self.cur.execute(Boiler._QUERY[query], args)

        return self.cur
        

    def loadTemplates(self, path=None):
        '''Loads boilerplate code template file info.

        If a path is not provided, it will default to the "paths"
        folder located in the source code directory
        '''

        if path is None:
            self.plates_path = self._getDefaultPlatesPath()
        else:
            self.plates_path = path

        self.con = sqlite3.connect(self.plates_path)
        self.cur = self.con.cursor()

    def supportedLanguages(self):
        '''Returns a sorted list of supported languages.'''

        return map(lambda x: x[0], self._getQuery('languages').fetchall())

    def supportedExtensions(self):
        '''Returns a sorted list of supported extensions.'''

        return map(lambda x: x[0], self._getQuery('extensions').fetchall())

    def _getTemplate(self, lang=None, ext=None):
        '''Returns the contents of a boilerplate template.
           
        First searches for a language match, and then extension
        '''

        template_text = None

        if ext is not None:
            ext = ext.lstrip('.')

        if lang is not None or ext is not None:
            row = self._getQuery('byEither', lang, ext).fetchone()

            if row is not None:
                template_text = row[0]
        
        return template_text

    def plate(self, lang=None, ext=None, funcs=[], name=None,
              newlines=False, spaces=0):
        '''Creates boilerplate code for a specific language.'''

        template = self._getTemplate(lang=lang, ext=ext)

        if template is None:
            if (lang or ext) is not None:
                raise LookupError('Unknown language or extension.')
            else:
                raise LookupError('Cannot generate boilerplate from info' \
                    ' provided. An extension or language is required.')

        # Create new plate
        plate = Plate(template)

        # Get text from plate
        boilerplateCode = plate.generate(name=name,
            funcs=funcs,
            newlines=bool(newlines),
            spaces=spaces)

        return boilerplateCode


class Plate:
    '''Boilerplate code generator.'''

    class _regex:
        name   = re.compile(r'\{BP_NAME\}')
        fname  = re.compile(r'\{BP_FNAME\}')
        func   = re.compile(
            r'\n?\{BP_FUNC_BEG\}(.*?)\{BP_FUNC_END\}\n?', re.DOTALL)
        break_ = re.compile(
            r'\{BP_BREAK_BEG\}\s*?\{BP_ALT_BEG\}(.*?)\{BP_ALT_END\}' \
             '\s*?\{BP_LINE_BEG\}(.*?)\{BP_LINE_END\}\s*?\{BP_BREAK_END\}',
            re.DOTALL)
        break_line = re.compile(r'\{BP_LINE_BEG\}(.*?)\{BP_LINE_END\}')

    default_classname = 'DEFAULT_NAME'

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''

        self.template = template

        # Extract function template
        fm = Plate._regex.func.search(template)
        self.function = fm.groups()[0] if fm else None

    def _newTemplate(self, name):
        '''Returns a template with the name filled in.'''

        if not name:
            name=Plate.default_classname

        return Plate._regex.name.sub(name, self.template)
    
    def _newFunction(self, name):
        '''Creates an empty function with the name filled in.'''

        return Plate._regex.fname.sub(name, self.function)

    def _insertFunctions(self, template, funcs=[]):
        '''Insert functions into template.'''

        functions = []

        for func in funcs:
            functions.append(self._newFunction(func))
        
        return Plate._regex.func.sub(''.join(functions), template)

    def _insertBreaks(self, template, newlines=False):
        replace = None

        if newlines:
            replace = r'\2'
        else:
            replace = r'\1'

        return Plate._regex.break_.sub(replace, template)

    def _replaceTabs(self, template, spaces=4):
        return template.expandtabs(spaces)

    def generate(self, name=None, funcs=[], newlines=False, spaces=0):
        '''Returns a custom boilerplate template.'''

        template = self._newTemplate(name)
        template = self._insertFunctions(template, funcs)
        template = self._insertBreaks(template, newlines=newlines)
        if spaces is not 0:
            template = self._replaceTabs(template, spaces)

        return template


def parse():
    '''Parses command line arguments'''

    import argparse

    # Main parser
    parser = argparse.ArgumentParser(
            description='Simple boilerplate code generator.')

    parser.add_argument('-E', '--lext', '--list-ext', '--list-extensions',
        action='store_true',
        help='List all %(prog)s\'s supported languages')

    parser.add_argument('-L', '--llang', '--list-lang', '--list-languages',
        action='store_true',
        help='List all %(prog)s\'s supported extensions')

    # Search parser
    searches = parser.add_argument_group('code selection')

    searches.add_argument('-e', '--ext', '--extension', metavar='EXTENSION',
        help='Explicitly name an extension to use.')

    searches.add_argument('-l', '--lang', '--language', metavar='LANGUAGE',
        help='Explicitly name a language to use.')

    # Generation parser
    options = parser.add_argument_group('code options')

    options.add_argument('--title', '--classname', metavar='NAME',
        help='Specify a class name / title for languages that use one' \
             ' (default: uses filename without extension)')

    options.add_argument('-f', '--force', action='store_true',
        help='Overwrite a file if one already exists' \
             ' (default: %(prog)s will exit with an error code of 2)')

    options.add_argument('-m', '--meth', '--method', action='append',
        default=[],
        metavar='METHOD',
        help='Generates an empty method (can be used multiple times)')

    options.add_argument('-n', '--line', '--newline', action='store_true',
        default=False,
        help='Use a newline after a function declaration' \
             ' (default: single space)')

    options.add_argument('-s', '--space', '--spaces', nargs='?',
        type=int, default=0, const=4, metavar='COUNT',
        help='Expand indentation into space characters' \
             ' (default: uses tab characters, or 4 spaces if a number is'
             ' not provided)')

    # Output parser
    output = parser.add_argument_group('output options')

    output.add_argument('-x', '--exec', '--executable', action='store_true',
        help='Attempts to make the file executable with chmod u+x')
    output.add_argument('file', nargs='?',
        help='Boilerplate file to be created. Returns filename for piping' \
             ' (default: print code to stdout)')

    return vars(parser.parse_args())

def main():
    import sys
    import stat

    # Prepare boiler templates
    parser = parse()

    if parser.get('help'):
        parser.print_help()
        return

    boiler = Boiler()

    if parser.get('llang'):
        print('\n'.join(boiler.supportedLanguages()))
    elif parser.get('lext'):
        print('\n'.join(boiler.supportedExtensions()))
    else:
        filepath = parser.get('file')

        name = None
        ext = None

        if parser.get('ext'):
            ext = parser.get('ext')
        elif filepath:
            filename = os.path.split(filepath)[1]
            name, ext = filename.rsplit('.', 1)

        if parser.get('classname'):
            name = parser.get('classname')

        try:
            # Generate boilerplate code
            text = boiler.plate(
                    ext      = ext,
                    lang     = parser.get('lang'),
                    funcs    = parser.get('meth'),
                    name     = name,
                    newlines = parser.get('line'),
                    spaces   = parser.get('space'))
        except LookupError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
            

        if filepath:
            textfile = None

            # Write output to file
            if parser.get('force'):
                textfile = open(filepath, 'w')
            else:
                try:
                    textfile = open(filepath, 'x')
                except FileExistsError:
                    print(
                        'File cannot be written because it already exists.' \
                        ' Use -f to overwrite.\n', file=sys.stderr)
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
