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

"""newskylabs/graphics/svg/library/svgicon.py:

A simple SVG icon - any SVG class like 'rect' or 'circle' can be
used...

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/28"

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class SVGIcon
## ---------------------------------------------------------

class SVGIcon():

    def __init__(self, *args, debug=1, **kwargs):
    
        # Store icon parameters
        self._debug  = debug
        self._args   = args
        self._kwargs = kwargs

    def toSVG(self):
        
        # Retrive parameters
        args   = self._args
        kwargs = self._kwargs

        # DEBUG
        if self._debug > 0:
            print("DEBUG SVGIcon:")
            print("  - args:   ", args)
            print("  - kwargs: ", kwargs)

        # Get icon's SVG tag 
        if 'tag' in kwargs:
            tag = kwargs['tag']
            del kwargs['tag']

        else:
            tag = 'rect'

        # Assemble SVG element
        icon = SVGElement(tag, **kwargs)

        return icon

## =========================================================
## =========================================================

## fin
