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

"""newskylabs/graphics/svg/library/circleicon.py:

An SVGElement subclass generating a simple icon assembled from 7 circles:

    o o
   o o o
    o o

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/23"

from math import pi, sin, cos

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class CircleIcon
## ---------------------------------------------------------

class CircleIcon():

    def __init__(self, 
                 x            = 0, 
                 y            = 0,
                 size         = 1, 
                 circle_size  = 1, 
                 color        = 'red', 
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
        
        # Icon center
        fx = radius
        fy = radius

        # Circle radius
        r = circle_size / 2

        # DEBUG
        if debug > 0:
            print("DEBUG NSLIcon:")
            print("")
            print("  - parameters:")
            print("    - debug:        {}".format(debug))
            print("    - x:            {}".format(x))
            print("    - y:            {}".format(y))
            print("    - size:         {}".format(size))
            print("    - circle_size:  {}".format(circle_size))
            print("    - color:        {}".format(color))
            print("")
            print("  - derived parameters:")
            print("    - radius:       {}".format(radius))
            print("    - fx:           {}".format(fx))
            print("    - fy:           {}".format(fy))
            print("")
            
        # A circle at the center
        self._icon.addCircle(cx=fx, cy=fy, r=r, fill=color)

        # 6 satellite circles
        segments = 6
        for i in range(segments):
            angle = i * 2 * pi / segments
            x = fx + cos(angle) * radius
            y = fy + sin(angle) * radius
            self._icon.addCircle(cx=x, cy=y, r=r, fill=color)
        
    def toSVG(self):
        return self._icon

## =========================================================
## =========================================================

## fin
