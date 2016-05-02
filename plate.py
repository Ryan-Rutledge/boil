#!/usr/bin/env python3

import re


class Plate:
    '''Boilerplate code generator.'''

    class regex:
        name  = re.compile(r'\{BP_NAME\}')
        fname = re.compile(r'\{BP_FNAME\}')
        func  = re.compile(r'\n\{BP_FUNC_BEG\}(.*)\{BP_FUNC_END\}\n', re.DOTALL)
        line  = re.compile(r'\{BP_LINE_BEG\}(.*?){BP_LINE_END\}', re.DOTALL)

    DEFAULT_NAME = 'DEFAULT_NAME'

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''

        self.template = template

        fm = Plate.regex.func.search(template)

        self.function = fm.groups()[0] if fm else None

    def newTemplate(self, name):
        '''Returns a template with the name filled in.'''

        if not name:
            name=Plate.DEFAULT_NAME

        return Plate.regex.name.sub(name, self.template)
    
    def newFunction(self, name):
        '''Creates an empty function with the name filled in.'''

        return Plate.regex.fname.sub(name, self.function)

    def insertFunctions(self, template, funcs=[]):
        '''Insert functions into template.'''

        functions = []

        for func in funcs:
            functions.append(self.newFunction(func))
        
        return Plate.regex.func.sub(''.join(functions), template)

    def insertBreaks(self, template, newlines=False):
        return Plate.regex.line.sub(r'\1' if newlines else ' ', template)

    def generate(self, name=None, funcs=[], newlines=False):
        '''Create a custom boilerplate template.'''

        template = self.newTemplate(name)
        template = self.insertFunctions(template, funcs)
        template = self.insertBreaks(template, newlines=newlines)

        return template
