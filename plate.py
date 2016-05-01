#!/usr/bin/env python3

import re

class Plate:
    '''Boilerplate code generator.'''

    tempname_regex = re.compile(r'\{BP_NAME_BEG\}(.*)\{BP_NAME_END\}')
    funcname_regex = re.compile(r'\{BP_FNAME_BEG\}(.*)\{BP_FNAME_END\}')
    function_regex = re.compile(r'\n\{BP_FUNC_BEG\}(.*)\{BP_FUNC_END\}\n', re.DOTALL)

    def extract(template, name=None):
        '''Returns a tuple with the beginning and end of a generic template and function.
           
        ([template_beg, template_end], [function_beg, function_end])
           
        template_beg
            A clean template up to function declarations

        template_end
            A clean template after function declarations
           
        function_beg
            A clean function template up to the name declaration

        function_end
            A clean function template after the name declaration

        '''

        cleanTemplate = template

        # Name match
        nm = Plate.tempname_regex.search(template)

        if nm:
            if not name:
                name = 'DEFAULT_NAME'
            cleanTemplate = Plate.tempname_regex.sub(name, template)

        template_beg = cleanTemplate
        template_end = ''
        function_beg = ''
        function_end = ''

        # Function match
        fm = Plate.function_regex.search(cleanTemplate)

        if fm:
            # Extract function from template
            template_beg = cleanTemplate[:fm.start()]
            template_end = cleanTemplate[fm.end():]

            # Function template
            functionTemplate = fm.groups()[0]

            # Function Name match
            fnm = Plate.funcname_regex.search(functionTemplate);

            if fnm:
                # Extract name from function template
                function_beg = functionTemplate[:fnm.start()]
                function_end = functionTemplate[fnm.end():]

        return ((template_beg, template_end), (function_beg, function_end))

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''
        
        self.template = template

        self.templateInfo, self.functionInfo = Plate.extract(template, name)

    def generate(self, options):
        '''Create a custom boilerplate template.'''

        funcs = options.get('func')

        functions = ''
        fbeg, fend = self.functionInfo

        if funcs and fbeg and fend:
            # Generate functions
            function_list = []
            for func in funcs:
                function_list.append(fbeg + func + fend)

            functions = ''.join(function_list)

        tbeg, tend = self.templateInfo
        template = tbeg + functions + tend

        return template
