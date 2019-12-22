## =========================================================
## Copyright 2019 Dietrich Bollmann
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##      http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## ---------------------------------------------------------

"""newskylabs/graphics/css/css.py:

A class for adding CSS style sections to SVG files.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/22"

from newskylabs.graphics.utils.general import formatKwargsKey

## =========================================================
## Utilities
## ---------------------------------------------------------

def _formatArg(arg):
    arg = str(arg)
    if ' ' in arg:
        arg = "'{}'".format(arg)
    return arg

def _formatArgs(args):
    return ' '.join([_formatArg(arg) for arg in args])

## =========================================================
## class CSSRule
## ---------------------------------------------------------

class CSSRule(object):

    def __init__(self, selector, *args, debug=False, **kwargs):

        if debug:
            print("DEBUG CSSClass.__init__(): selector: {}, args: {}, kwargs: {}" \
                  .format(selector, args, kwargs))

        self._debug = debug
        self._selector = formatKwargsKey(selector)
        self._attrs = {}
            
        # Add keyword args as XML attributes
        for name, value in kwargs.items():
            if self._debug:
                print("DEBUG CSSClass.__init__(): {}: {}"\
                      .format(name, value))
            self._addAttr(name, value)
        
    def _addAttr(self, name, value):

        if self._debug:
            print("DEBUG CSSClass._addAttr(): {}: {}" \
                  .format(name, value))

        name = formatKwargsKey(name)
        self._attrs[name] = value

    def __getattr__(self, name):

        if self._debug:
            print("DEBUG CSSClass.__getattr__(): {}" \
                  .format(name))

        def addAttr(*args, **kwargs):

            if self._debug:
                print("DEBUG CSSClass.addAttr(): args: {}, kwargs: {}" \
                      .format(name, args, kwargs))
            
            value = _formatArgs(args)
            self._addAttr(name, value)
            return self

        return addAttr

    def tostring(self, level):

        indent = ' ' * (2 * level)
        
        # Two blanks initial indent
        css = '  {} {{\n'.format(self._selector)
        for key, value in self._attrs.items():
            css += indent + '    {}: {};\n'.format(key, value)
        css += indent + '  }\n'

        # Indent for closing </style> or next CSS rule 
        css += indent

        return css

## =========================================================
## =========================================================

## fin.
