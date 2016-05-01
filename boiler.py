#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(__file__))
from plate import Plate

'''Boilerplate code template manager.'''

plates = None      # bidirectional dict of template names/extensions
plates_path = None # Absolute path to boilerplate templates

def loadTemplates(path):
    '''Loads boilerplate code template file info.'''

    global plates
    global plates_path

    plates_path = path
    # Get list of boilerplate template files
    template_list = os.listdir(plates_path)
    template_list.sort(reverse=True)

    plates = {}
    for template in template_list:
        # Add an entry for template filetype/extension
        file_name, file_ext = os.path.splitext(template)
        plates[file_name] = file_ext
        plates[file_ext] = file_name

def getTemplate(templatename):
    '''Returns the contents of a boilerplate template.'''
    
    template_path = os.path.join(plates_path, templatename)
        
    template = open(template_path)
    template_text = template.read()
    template.close()
    
    return template_text
    
def getUnknownTemplate(platetype=None, ext=None):
    '''Calls getTemplate on the appropriate boilerplate template.'''

    if platetype:
        ext = plates.get(platetype)

        # Check if extension was found
        if not ext:
            raise ValueError('No template found for language "{0}"'.format(platetype))
    elif ext:
        platetype = plates.get(ext)

        # Check if platetype was found
        if not platetype:
            raise ValueError('No template found for extension "{0}"'.format(ext))
    else:
        raise ValueError("Unable to generate boilerplate. No language or extension provided")
    
    return getTemplate(platetype + ext)

def plate(filename, **options):
    '''Creates boilerplate code for a specific language.

    options: function language tabwidth executable name std
    '''

    template = ''

    # Get template contents
    lang = options.get('language')
    if (lang):
        template = getUnknownTemplate(lang)
    else:
        ext = os.path.splitext(filename)[1]
        template = getUnknownTemplate(ext=ext)

    # Create new plate
    plate = Plate(template, options.get('name'))

    # Get text from plate
    boilerplateCode = plate.generate(options)

    return boilerplateCode
