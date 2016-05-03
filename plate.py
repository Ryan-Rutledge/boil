#!/usr/bin/env python3

import re


class Plate:
    '''Boilerplate code generator.'''

    class _regex:
        name   = re.compile(r'\{BP_NAME\}')
        fname  = re.compile(r'\{BP_FNAME\}')
        func   = re.compile(
                    r'\n\{BP_FUNC_BEG\}(.*?)\{BP_FUNC_END\}\n', re.DOTALL)
        break_ = re.compile(
                    r'\{BP_BREAK_BEG\}\s*?\{BP_ALT_BEG\}(.*?)\{BP_ALT_END\}\s*?\{BP_LINE_BEG\}(.*?)\{BP_LINE_END\}\s*?\{BP_BREAK_END\}',
                    re.DOTALL)
        break_line = re.compile(r'\{BP_LINE_BEG\}(.*?)\{BP_LINE_END\}')
        tabs   = re.compile(r'\t')

    default_classname = 'DEFAULT_NAME'

    def __init__(self, template, name=None):
        '''Convert template into a useful object.'''

        self.template = template

        # Extract function template
        fm = Plate._regex.func.search(template)
        self.function = fm.groups()[0] if fm else None

    def _newTemplate(self, name):
        '''Returns a template with the name filled in.'''

        if not name:
            name=Plate.default_classname

        return Plate._regex.name.sub(name, self.template)
    
    def _newFunction(self, name):
        '''Creates an empty function with the name filled in.'''

        return Plate._regex.fname.sub(name, self.function)

    def _insertFunctions(self, template, funcs=[]):
        '''Insert functions into template.'''

        functions = []

        for func in funcs:
            functions.append(self._newFunction(func))
        
        return Plate._regex.func.sub(''.join(functions), template)

    def _insertBreaks(self, template, newlines=False):
        replace = None

        if newlines:
            replace = r'\2'
        else:
            replace = r'\1'

        return Plate._regex.break_.sub(replace, template)

    def _replaceTabs(self, template, spaces=4):
        return Plate._regex.tabs.sub(' '*spaces, template)

    def generate(self, name=None, funcs=[], newlines=False, spaces=0):
        '''Returns a custom boilerplate template.'''

        template = self._newTemplate(name)
        template = self._insertFunctions(template, funcs)
        if spaces is not 0:
            template = self._replaceTabs(template, spaces)
        template = self._insertBreaks(template, newlines=newlines)

        return template
