#!/usr/bin/env python3

import re

class Plate:
    '''Boilerplate code generator.'''

    tempname_regex = re.compile(r'\{BP_NAME_BEG\}(.*)\{BP_NAME_END\}')
    funcname_regex = re.compile(r'\{BP_FNAME_BEG\}(.*)\{BP_FNAME_END\}')
    function_regex = re.compile(r'\n\{BP_FUNC_BEG\}(.*)\{BP_FUNC_END\}\n', re.DOTALL)

    DEFAULT_NAME = 'DEFAULT_NAME'

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''

        self.template = template

        fm = Plate.function_regex.search(template)

        self.function = fm.groups()[0] if fm else None

    def newTemplate(self, name):
        '''Returns a template with the name filled in.'''

        if not name:
            name=Plate.DEFAULT_NAME

        return Plate.tempname_regex.sub(name, self.template)
    
    def newFunction(self, name):
        '''Creates an empty function with the name filled in.'''

        return Plate.funcname_regex.sub(name, self.function)

    def insertFunctions(self, template, funcs=[]):
        '''Insert functions into template.'''

        functions = []

        for func in funcs:
            functions.append(self.newFunction(func))
        
        return Plate.function_regex.sub(''.join(functions), template)

    def generate(self, name=None, funcs=[]):
        '''Create a custom boilerplate template.'''

        template = self.newTemplate(name)
        template = self.insertFunctions(template, funcs)
        #template = insertLines(template)

        return template
