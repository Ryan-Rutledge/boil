#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(__file__))
from plate import Plate

'''Boilerplate code template manager.'''

plates = None      # bidirectional dict of template names/extensions
plates_path = None # Absolute path to boilerplate templates
plate_ext = set()
plate_lan = set()

def loadTemplates(path):
    '''Loads boilerplate code template file info.'''

    global plates
    global plates_path

    plates_path = path
    # Get list of boilerplate template files
    template_list = os.listdir(plates_path)
    template_list.sort(reverse=True)

    plates = {}
    plate_ext.clear()
    plate_lan.clear()
    # Add entries for template filetype/extension
    for template in template_list:
        file_name, file_ext = os.path.splitext(template)

        plates[file_name] = file_ext
        plates[file_ext] = file_name

        plate_lan.add(file_name)
        plate_ext.add(file_ext)

def supportedLanguages():
    langs = list(plate_lan)
    langs.sort()

    return langs

def supportedExtensions():
    exts = list(plate_ext)
    exts.sort()

    return exts

def getTemplate(query):
    '''Returns the contents of a boilerplate template.
       
    Accepts either a language or a file extension parameter.
    '''

    templatename = [plates.get(query), query]
    
    if not templatename[0]:
        sys.stderr.write('No boilerplate code found for {0}.\n'.format(query))
        sys.exit(3)
    else:
        if query[0] != '.':
            templatename.reverse()
            
        template_path = os.path.join(plates_path, ''.join(templatename))
        template = open(template_path)
        template_text = template.read()
        template.close()
    
    return template_text

def plate(filename=None, lang=None, functions=[]):
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
    template = getTemplate(query)

    # Create new plate
    plate = Plate(template, name)

    # Get text from plate
    boilerplateCode = plate.generate(funcs=functions)

    return boilerplateCode
