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

def getTemplate(query):
    '''Returns the contents of a boilerplate template.
       
    Accepts either a language or a file extension parameter.
    '''

    templatename = [plates.get(query), query]
    
    if not templatename[0]:
        print('No boilerplate code found for', query)
        sys.exit(1)
    else:
        if query[0] != '.':
            templatename.reverse()
            
        template_path = os.path.join(plates_path, ''.join(templatename))
        template = open(template_path)
        template_text = template.read()
        template.close()
    
    return template_text

def plate(filename=None, options={}):
    '''Creates boilerplate code for a specific language.

    options: function language tabwidth executable name std
    '''

    template = ''

    query = options.get('lang')
    if not query:
        if filename:
            query = os.path.splitext(filename)[1]
        else:
            print("Not enough information was provided to generate boilerplate.")
            sys.exit(1)

    # Get template
    template = getTemplate(query)

    # Create new plate
    plate = Plate(template, options.get('name'))

    # Get text from plate
    boilerplateCode = plate.generate(funcs=options.get('meth'))

    return boilerplateCode
