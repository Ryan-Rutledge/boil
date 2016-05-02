#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(__file__))
from plate import Plate

templateDirectory = 'plates'

class Boiler:
    '''Boilerplate code template manager.'''

    def __init__(self, template_directory):
        self.plates = None      # bidirectional dict of template names/extensions
        self.plates_path = None # Absolute path to boilerplate templates
        self.plate_ext = set()
        self.plate_lan = set()

        self.loadTemplates(template_directory)

    def loadTemplates(self, path):
        '''Loads boilerplate code template file info.'''

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

    def getTemplate(self, query):
        '''Returns the contents of a boilerplate template.
           
        Accepts either a language or a file extension parameter.
        '''

        templatename = [self.plates.get(query), query]
        
        if not templatename[0]:
            sys.stderr.write('No boilerplate code found for {0}.\n'.format(query))
            sys.exit(3)
        else:
            if not query.startswith('.'):
                templatename.reverse()
                
            template_path = os.path.join(self.plates_path, ''.join(templatename))
            template = open(template_path)
            template_text = template.read()
            template.close()
        
        return template_text

    def plate(self, filename=None, lang=None, functions=[], override_name=None, newlines=False):
        '''Creates boilerplate code for a specific language.'''

        template = ''

        name = None
        ext = None
        query = None

        if filename:
            name, ext = os.path.splitext(filename)

        if lang:
            query = lang
        elif ext:
            query = ext
        else:
            sys.stderr.write("Not enough information was provided to generate boilerplate.\n")
            sys.exit(1)

        # Get template
        template = self.getTemplate(query)

        # Create new plate
        plate = Plate(template)

        # Get text from plate
        if override_name:
            name = override_name
        boilerplateCode = plate.generate(name, functions, newlines=bool(newlines))

        return boilerplateCode
