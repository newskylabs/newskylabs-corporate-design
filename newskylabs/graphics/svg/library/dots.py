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

"""newskylabs/graphics/svg/library/dots.py:

An SVG plugin to render a dotted Pattern.  In the middle of the
pattern a QR-Code is rendered, which encodes a vcard containing the
personal information from the front side of the meishi.

Used as back side of name cards.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/28"

from newskylabs.graphics.svg.svg import SVGElement
from newskylabs.graphics.svg.library.plugin import SVGPlugin

## =========================================================
## class Dots
## ---------------------------------------------------------

class Dots(SVGPlugin):

    def __init__(self, 
                 *args, 
                 x=0, y=0, width='100', height='100',
                 **kwargs):

        # DEBUG
        # When a debug level has been given in kwargs
        # overwrite the debug level.
        if 'debug' in kwargs \
           and 'level' in kwargs['debug']:
            debug = kwargs['debug']['level']
        self._debug = debug

        self._geometry = x, y, width, height

        if debug > 0:
            print("DEBUG ConPat.__init__():")
            print("")
            print("  - debug level: {}".format(debug))
            print("  - args:        {}".format(args))
            print("  - kwargs:      {}".format(kwargs))
            print("  - x:           {}".format(x))
            print("  - y:           {}".format(y))
            print("  - width:       {}".format(width))
            print("  - height:      {}".format(height))

        super().__init__(*args, **kwargs)
        
    def toSVG(self):

        # Retrive parameters
        args   = self._args
        kwargs = self._kwargs
        x, y, width, height = self._geometry

        # Retrive the parameters
        # necessary to calculate the geometry of the connection pattern
        color       = kwargs['color']
        background  = kwargs['background']
        dotsize     = kwargs['dotsize']

        # Depending on the debug level, either a small margin is shown
        # (normally a 1mm margin needed as tolerance when cutting the
        # name cards) or a large margin to better see and debug the
        # part of the pattern rendered outside of the name card.
        if self._debug == 0:
            margin = kwargs['parameter']['margin']
        else:
            margin = kwargs['debug']['margin']
        
        # DEBUG
        if self._debug > 0:
            print("DEBUG ConPat.toSVG():")
            print("")
            print("  - margin:      {}  (depends on debug level)".format(margin))
            print("  - color:       {}".format(color))
            print("  - background:  {}".format(background))
            print("  - dotsize:     {}".format(dotsize))
            print("")
           
        # Grid parameters
        nx = 20
        ny = 15
            
        # Vertex parameters
        r = dotsize / 2
        
        # Extra padding
        # used to show more of the vertices 
        # - at the outer border by shrinking the whole pattern
        # - at the QR-Code border by shrinking the QR-Code
        extra_padding = r / 3
            
        # The distance / increment is calculated by
        # deviding the size through the number of vertices - 1
        ix = (width  - 2 * extra_padding) / (nx - 1)
        iy = (height - 2 * extra_padding) / (ny - 1)
        
        # The initial circle positons
        nix = 0
        niy = 0
        
        # Padding vertical
        yu = niy + extra_padding
        yd = height - niy
        dy = yd - yu
            
        # Padding horizontal
        xl = nix + extra_padding
        xr = width - nix
        dx = xr - xl
            
        # Showing a margin around the meishi
        width_with_margin  = width  + 2 * margin
        height_with_margin = height + 2 * margin

        # The root element of the SVG plugin
        plugin = SVGElement('g')

        # When a background color is given add a background rectangle;
        # 'None' results in a transparent background.
        if background != None:
            plugin.addRect(
                width  = width_with_margin,
                height = height_with_margin,
                fill   = background
            )
        
        # Translate according to the margin
        e = plugin.addTranslate(x=x, y=y)
    
        # When in debug mode, visualize the original size of the
        # meishi with a gray frame.  The margin outside the frame is
        # intended to be cut off after the meishis have been printed.
        if self._debug > 0:
            e.addRect(
                width        = width, 
                height       = height,
                stroke       = 'gray',
                stroke_width = 0.1,
                fill         = 'none'
            )

        # Calculate vertex positions
        vertices = []
        y = yu
        for row in range(ny):
        
            # Indent every second row
            x = xl
            if row % 2 != 0:
                x += ix / 2
        
            vertices_row = []
            n = nx - 1 if row % 2 else nx
            for col in range(n):
                vertices_row.append((x, y))
                x += ix
        
            vertices.append(vertices_row)
            y += iy
        
        # Draw vertices
        for row in range(ny):
            n = nx - 1 if row % 2 else nx
            for col in range(n):
                x, y = vertices[row][col]
                e.addCircle(cx=x, cy=y, r=r, fill=color)
        
        # Some more padding to show a little bit more of the vertices
        # touching the border of the QR-Code.  
        # Here again we are using the value given as 'extra_padding',
        # which was first defined in order to shrink and translate the
        # whole pattern so that slightly more of the vertices touching
        # the outer sides of the meishi are shown.
        padding_y = iy + (2 * extra_padding)
        
        size_y = height - 2 * padding_y
        ry = padding_y
        
        padding_x = 4.5 * ix + (2 * extra_padding)
        size_x = width - 2 * padding_x
        rx = padding_x
            
        e = e.addTranslate(x=rx, y=ry)
        
        # Add a white background for the QR-Code
        rect = e.addRect(
            width  = size_x, 
            height = size_y,
            fill   = 'white'
        )
        
        # When the background is white or transparent a frame will be
        # added around the white background for the QR-Code
        if background == None \
           or background == 'none' \
           or background == 'white':
            rect = e.addRect(
                width        = size_x,
                height       = size_y,
                stroke       = color,
                stroke_width = 0.2,
                fill         = 'none'
            )
        
        # Append the QR-Code
        # Retrive the personal data
        # necessary to generate the QR-Code
        vcard_data = kwargs['content']
        e.addQRCode(
            vcard_data,
            width  = size_x,
            height = size_y,
        )

        return plugin

## =========================================================
## =========================================================

## fin
