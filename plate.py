#!/usr/bin/env python3

import re

class Plate:
    '''Boilerplate code generator.'''

    function_extractor = re.compile(r'{BP_FUNCTION_START}(.*){BP_FUNCTION_END}', re.DOTALL)
    funcname_extractor = re.compile(r'{BP_FNAME_START}(.*){BP_FNAME_END}')
    tempname_extractor = re.compile(r'{BP_NAME_START}(.*){BP_NAME_END}')

    def extract(template, name=None):
        '''Returns a tuple with a template and function and inject points.
           
        ((template, functionInject), (functionTemplate, nameInject))
           
        template
            A clean template, with no functions

        functionInject
            Char count from start of template to function insertion

        functionTemplate
            A nameless, void function

        nameInject
            Char count from start of functionTemplate to name insertion
        '''

        cleanTemplate    = template
        functionInject   = None
        functionTemplate = None
        nameInject       = None

        # Name match
        nm = Plate.tempname_extractor.search(template)

        if nm:
            if not name:
                name = 'DEFAULT_NAME'
            cleanTemplate = Plate.tempname_extractor.sub(name, template)

        # Function match
        fm = Plate.function_extractor.search(cleanTemplate)
        if fm:
            functionInject = fm.start()

            # Extract function from template
            cleanTemplate = cleanTemplate[:functionInject] + cleanTemplate[:fm.end()]

            # Function template
            functionTemplate = fm.groups()[0]

            # Function Name match
            fnm = Plate.funcname_extractor.search(functionTemplate);
            if fnm:
                nameInject = fnm.start()

                # Extract name from function template
                functionTemplate = functionTemplate[:nameInject] + functionTemplate[:fnm.end()]

        return ((cleanTemplate, functionInject), (functionTemplate, nameInject))

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''
        
        self.template = template

        self.templateInfo, self.functionInfo = Plate.extract(template, name)

    def generate(self, options):
        '''Create a custom boilerplate template.'''

        return self.templateInfo[0]
