#!/usr/bin/env python3

import os
import sys
from plate import Plate


class Boiler:
    '''Boilerplate code template manager.'''

    default_template_directory = 'plates'

    def __init__(self, template_directory=None):
        self.plates = None      # bidirectional dict of template names/extensions
        self.plates_path = None # Absolute path to boilerplate templates
        self.plate_ext = set()
        self.plate_lan = set()

        self.loadTemplates(template_directory)

    def loadTemplates(self, path=None):
        '''Loads boilerplate code template file info.'''

        # If a path is not provided, use the source code directory
        if path is None:
            from inspect import getsourcefile

            # Get path of current code
            source_file = os.path.abspath(getsourcefile(lambda:None))

            # Get directory of current code
            source_dir = os.path.split(source_file)[0]

            # Get directory of boilerplate templates
            self.plates_path = os.path.join(source_dir, Boiler.default_template_directory)
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

    def getTemplate(self, lang=None, ext=None):
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

        if template_name is not None:
            template_path = os.path.join(self.plates_path, ''.join(template_name))

            with open(template_path) as template:
                template_text = template.read()
        
        return template_text

    def plate(self, lang=None, ext=None, functions=[], name=None, newlines=False):
        '''Creates boilerplate code for a specific language.'''

        template = self.getTemplate(ext=ext, lang=lang)

        if template is None:
            if (lang or ext) is not None:
                sys.stderr.write('No template found for the extension or language provided.')
                sys.exit(3)
            else:
                sys.stderr.write("Not enough information was provided to generate boilerplate.\n")
                sys.exit(1)

        # Create new plate
        plate = Plate(template)

        # Get text from plate
        boilerplateCode = plate.generate(name, functions, newlines=bool(newlines))

        return boilerplateCode
