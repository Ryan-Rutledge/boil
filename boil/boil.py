#!/usr/bin/env python3

import re
import os
import sys
import stat
import argparse

class Boiler:
    '''Boilerplate code template manager.'''

    def_plate_dir = 'plates'

    def __init__(self, template_directory=None):
        self.plates = None      # bidirectional dict names/extensions
        self.plates_path = None # Absolute path to boilerplate templates
        self.plate_ext = set()
        self.plate_lan = set()

        self.loadTemplates(template_directory)

    def loadTemplates(self, path=None):
        '''Loads boilerplate code template file info.

        If a path is not provided, it defaults to the source code directory
        '''

        if path is None:
            from inspect import getsourcefile

            # Get path of current code
            source_file = os.path.abspath(getsourcefile(lambda:None))

            # Get directory of current code
            source_dir = os.path.split(source_file)[0]

            # Get directory of boilerplate templates
            self.plates_path = os.path.join(source_dir, Boiler.def_plate_dir)
        else:
            self.plates_path = path

        # Get list of boilerplate template files
        template_list = os.listdir(self.plates_path)
        template_list.sort(reverse=True)

        self.plates = {}
        self.plate_ext.clear()
        self.plate_lan.clear()
        # Add entries for template filetype/extension
        for template in template_list:
            file_name, file_ext = os.path.splitext(template)

            self.plates[file_name] = file_ext
            self.plates[file_ext] = file_name

            self.plate_lan.add(file_name)
            self.plate_ext.add(file_ext)

    def supportedLanguages(self):
        '''Returns a sorted list of supported languages.'''

        langs = list(self.plate_lan)
        langs.sort()

        return langs

    def supportedExtensions(self):
        '''Returns a sorted list of supported extensions.'''

        exts = list(self.plate_ext)
        exts.sort()

        return exts

    def _getTemplate(self, lang=None, ext=None):
        '''Returns the contents of a boilerplate template.
           
        First searches for a language match, and then extension
        '''

        template_name = None

        # Look for language template
        if lang is not None:
            tmp_ext = self.plates.get(lang)

            if tmp_ext is not None:
                template_name = lang + tmp_ext

        # Look for extension template
        if template_name is None and ext is not None:
            tmp_lang = self.plates.get(ext)
            
            if tmp_lang is not None:
                template_name = tmp_lang + ext

        template_text = None
        if template_name is not None:
            template_path = os.path.join(self.plates_path, template_name)

            with open(template_path) as template:
                template_text = template.read()
        
        return template_text

    def plate(self, lang=None, ext=None, funcs=[], name=None,
              newlines=False, spaces=0):
        '''Creates boilerplate code for a specific language.'''

        template = self._getTemplate(ext=ext, lang=lang)

        if template is None:
            if (lang or ext) is not None:
                sys.stderr.write('Unknown language or extension.\n')
                sys.exit(3)
            else:
                sys.stderr.write(
                    'Cannot generate boilerplate from info' \
                    ' provided. An extension or language is required.\n')
                sys.exit(1)

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
        tabs   = re.compile(r'\t')

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
        return Plate._regex.tabs.sub(' '*spaces, template)

    def generate(self, name=None, funcs=[], newlines=False, spaces=0):
        '''Returns a custom boilerplate template.'''

        template = self._newTemplate(name)
        template = self._insertFunctions(template, funcs)
        template = self._insertBreaks(template, newlines=newlines)
        if spaces is not 0:
            template = self._replaceTabs(template, spaces)

        return template

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

    options.add_argument('--classname', '--title',
        help='Specify a class name / title for languages that use one' \
             ' (default: uses filename without extension)')

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

    options.add_argument('-s', '--space', '--spaces', nargs='?',
        type=int, default=0, const=4, metavar='COUNT',
        help='Expand indentation into space characters' \
             ' (default: uses tab characters, or 4 spaces if a number is'
             ' not provided )')

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
                newlines=parser.get('line'),
                spaces=parser.get('space'))

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
