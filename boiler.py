#!/usr/bin/env python3

import os
import sys
from inspect import getsourcefile

class boiler():
    '''Boilerplate code template manager.'''

    plates = None      # bidirectional dict of template names/extensions
    plates_path = None # Absolute path to boilerplate templates

    def loadTemplates():
        '''Loads boilerplate code template file info.'''

        # Get path of current code
        source_file = os.path.abspath(getsourcefile(lambda:None))
        # Get directory of current code
        source_dir = os.path.split(source_file)[0]
        # Get directory of boilerplate templates
        boiler.plates_path = os.path.join(source_dir, 'plates')
        # Get list of boilerplate template files
        template_list = os.listdir(boiler.plates_path)
        template_list.sort(reverse=True)

        boiler.plates = {}
        for template in template_list:
            # Add an entry for template filetype/extension
            file_name, file_ext = os.path.splitext(template)
            boiler.plates[file_name] = file_ext
            boiler.plates[file_ext] = file_name

    def getTemplate(templatename):
        '''Returns the contents of a boilerplate template.'''
        
        template_path = os.path.join(boiler.plates_path, templatename)
            
        template = open(template_path)
        template_text = template.read()
        template.close()
        
        return template_text
        
    def getUnknownTemplate(platetype=None, ext=None):
        '''Calls boiler.getTemplate on the appropriate boilerplate template.'''

        if platetype:
            ext = boiler.plates.get(platetype)

            # Check if extension was found
            if not ext:
                raise ValueError('No template found for language "{0}"'.format(platetype))
        elif ext:
            platetype = boiler.plates.get(ext)

            # Check if platetype was found
            if not platetype:
                raise ValueError('No template found for extension "{0}"'.format(ext))
        else:
            raise ValueError("Unable to generate boilerplate. No language or extension provided")
        
        return boiler.getTemplate(platetype + ext)

    def write(text, filename):
        '''Copies text into a new file.'''

        textfile = open(filename, 'x')
        print(tempfile.read(), end='', file=textfile)
        
        textfile.close()

    def plate(filename, **options):
        '''Creates boilerplate code for a specific language.

        options: function language tabwidth executable
        '''

        template = ''

        # Get template contents
        lang = options.get('language')
        if (lang):
            template = boiler.getUnknownTemplate(lang)
        else:
            ext = os.path.splitext(filename)[1]
            template = boiler.getUnknownTemplate(ext=ext)
        print(template)

        # Create new plate
        #newPlate = Plate(template)

        # Get text from plate
        #boiler.write(template, filename)
        # open editor

def main():
    # TODO: when creating boilerplate, check for --create and --editor flags
    boiler.loadTemplates()
    #boiler.plate('tmp.py')

if __name__ == '__main__':
    main()
