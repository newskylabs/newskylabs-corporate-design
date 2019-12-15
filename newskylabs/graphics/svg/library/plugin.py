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

"""newskylabs/graphics/svg/library/plugin.py:

A minimal SVG plugin.

To be used as parent class for SVG plugins.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/15"

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class SVGPlugin
## ---------------------------------------------------------

class SVGPlugin:

    def __init__(self, *args, **kwargs):
    
        # Store plugin parameters
        self._args   = args
        self._kwargs = kwargs

    def toSVG(self):
        
        # Retrive parameters
        args   = self._args
        kwargs = self._kwargs

        # DEBUG
        print("DEBUG SVGIcon:")
        print("  - args:   ", args)
        print("  - kwargs: ", kwargs)

        # A minimal praphical representation
        tag = 'rect'
        plugin = SVGElement(
            tag, 
            x            = 0, 
            y            = 0, 
            width        = 10,
            height       = 10, 
            fill         = 'pink', 
            stroke       = 'black', 
            stroke_width = 1
        )

        return plugin

## =========================================================
## =========================================================

## fin.
