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

"""newskylabs/graphics/svg/library/nslicon.py:

An SVGElement subclass for rendering the NewSkyLabs icon.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/26"

from math import pi, sin, cos

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class NSLIcon
## ---------------------------------------------------------

class NSLIcon():

    def __init__(self, 
                 x            = 0, 
                 y            = 0,
                 size         = 10, 
                 color        = 'red', 
                 stroke_width = 1,
                 debug        = 0
    ):

        # Icon position
        if x != 0 or y != 0:
            transform = 'translate({:.3f}, {:.3f})'.format(x, y)
            self._icon = SVGElement('g', transform=transform)
        else:
            self._icon = SVGElement('g')

        # Icon radius
        radius = size / 2.0
        
        # DEBUG
        if debug > 0:
            print("DEBUG NSLIcon:")
            print("")
            print("  - parameters:")
            print("    - x:            {}".format(x))
            print("    - y:            {}".format(y))
            print("    - size:         {}".format(size))
            print("    - color:        {}".format(color))
            print("    - stroke_width: {}".format(stroke_width))
            print("    - debug:        {}".format(debug))
            print("")
            print("  - derived parameters:")
            print("    - radius:       {}".format(radius))
            print("")
            
        # Calculate vertex positions
        vertices = []
        segments = 6
        for i in range(segments):
            angle = i * 2 * pi / segments
            x = cos(angle) * radius
            y = sin(angle) * radius
            vertices.append((x, y))
        
        # Naming the vertices
        #         
        #      ul--ur
        #     / \ / \
        #    ml--c---mr
        #     \ / \ /
        #      ll--lr
        #      
        c = (0, 0)
        ul = vertices[4]
        ur = vertices[5]
        ml = vertices[3]
        mr = vertices[0]
        ll = vertices[2]
        lr = vertices[1]
        
        # Connecting the vertices to form the NewSkyLabs icon
        for path in [(mr, ul, ml, ll, mr),
                     (ml, ur, mr, lr, ml),
                     (ul, lr),
                     (ll, ur),
                    ]:
                
            self._icon.addPath(
                path            = path,
                stroke          = color, 
                stroke_width    = stroke_width,
                close_path      = False,
                stroke_linejoin = 'miter',
                stroke_linecap  = 'round',
                fill            = None,
            )

    def toSVG(self):
        return self._icon

## =========================================================
## =========================================================

## fin
