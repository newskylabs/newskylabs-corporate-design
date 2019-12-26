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

"""newskylabs/graphics/svg/library/conicon.py:

CONnection Icon class.

Seven vertices which can be connected in all possible ways.

      5   6

    4   0   1

      3   2

The vertices can be rendered as a cycle
depending on the 'circle_pattern' parameter:

  - The i-th letter encodes the i-th vertex;
  - a 'o' results in the vertex being rendered as a circle;
  - a '-' results in the vertex not being rendered.

Examples:

  - circle_pattern: -------      None of the circle is rendered
  - circle_pattern: o-o-o-o      The center vertex and the vertices 2, 4, 6 are rendered
  - circle_pattern: ooooooo      All circles are rendered

The vertices can be connected by paths 
depending on the 'connection_pattern' given:

  - 135 stands for a path from vertex 1 to vertex 3 and then further
    to vertex 5;

  - 135c the terminal 'c' results in "closing" the path, i.e. a path
    back from vertex 5 to vertex 1.

Examples:

  connection_pattern: 123456c    vertex 1 is connected with vertex 2;
                                 vertex 2 is connected with vertex 3;
                                 ...
                                 vertex 5 is connected with vertex 6;
                                 the 'c' results in a connection 
                                 from the last to the first vertex, therefore
                                 vertex 6 is connected with vertex 1.

  connection_pattern: 25 36      vertex 2 is connected with vertex 5;
                                 vertex 3 is connected with vertex 6.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/25"

from math import pi, sin, cos

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class CONIcon
## ---------------------------------------------------------

class CONIcon():
    """CONnection Icon class."""

    def __init__(self, 
                 x                  = 0, 
                 y                  = 0,
                 size               = 10, 
                 color              = 'black',
                 stroke_width       = 1,
                 circle_size        = 3,
                 circle_pattern     = 'ooooooo',
                 connection_pattern = '123456c 14 25 36',
                 debug              = 1
    ):
    
        self._x                  = x
        self._y                  = y
        self._size               = size
        self._color              = color
        self._stroke_width       = stroke_width
        self._circle_size        = circle_size
        self._circle_pattern     = circle_pattern
        self._connection_pattern = connection_pattern
        self._debug              = debug
      
    def toSVG(self):

        x    = self._x
        y    = self._y
        size = self._size

        # Radius of sattelite orbit
        pattern_radius = size / 2
        
        # Vertices
        #         
        #      5---6
        #     / \ / \
        #    4---0---1
        #     \ / \ /
        #      3---2

        # Center vertex (0)
        vertices = [(x, y)]

        # Satellites (1-6)
        num_satellites = 6
        for i in range(num_satellites):
        
            angle = i * 2 * pi / num_satellites
            px = x + cos(angle) * pattern_radius
            py = y + sin(angle) * pattern_radius
        
            # Add satellite  position to stroke from satellite to satellite
            vertices.append((px, py))

        # Store the vertex positions for later use
        self._vertices = vertices

        # Assemble the SVG pattern
        pattern = SVGElement('g')
        self.add_connection_pattern(pattern)
        self.add_circle_pattern(pattern)

        # Return the root element of the pattern
        return pattern

    def add_connection_pattern(self, parent):

        vertices     = self._vertices
        conpat       = self._connection_pattern
        color        = self._color
        stroke_width = self._stroke_width
        
        if not conpat:
            return

        # '14 25 36 123456c' -> ['14', '25', '36', '123456c']
        cpaths = conpat.strip().split(' ')
        for cpath in cpaths:

            # Close the path when the last character is c
            if cpath[-1] == 'c':
                close_path = True
                cpath = cpath[:-1]
            else:
                close_path = False

            # Translate the index list to a list of vertices
            path = []
            for v in cpath:
                vi = int(v)
                vertex = vertices[vi]
                path.append(vertex)

            # Add the path
            parent.addPath(
                path           = path, 
                close_path     = close_path,
                stroke         = color,
                stroke_width   = stroke_width, 
                stroke_linecap = 'miter',
                fill           = 'none'
            )

    def add_circle_pattern(self, parent):

        vertices      = self._vertices
        circlepat     = self._circle_pattern
        circle_radius = self._circle_size / 2
        color         = self._color

        if not circlepat:
            return

        l = len(circlepat)
        for vi in range(len(vertices)):
            if vi < l and circlepat[vi] == 'o':
                x, y = vertices[vi]
                parent.addCircle(cx=x, cy=y, r=circle_radius, fill=color)
            vi += 1

## =========================================================
## =========================================================

## fin
