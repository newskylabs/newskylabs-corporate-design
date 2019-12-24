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

A dotted Pattern SVG plugin containing a QR-Code encoding a vcard
with the personal information written on the name card.

Used as back side of name cards.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/24"

from newskylabs.graphics.svg.svg import SVGElement
from newskylabs.graphics.svg.library.plugin import SVGPlugin

## =========================================================
## class Simple
## ---------------------------------------------------------

class SimpleBackside(SVGPlugin):

    def __init__(self, 
                 *args, 
                 x=0, y=0, width='10', height='10',
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
        qrcode_size = kwargs['qrcode_size']

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
            print("  - qrcode_size: {}".format(qrcode_size))
            print("")
           
        # Showing a margin around the meishi
        width_with_margin  = width  + 2 * margin
        height_with_margin = height + 2 * margin

        # The root element of the SVG plugin
        plugin = SVGElement('g')

        # When a background has been given add a background rectangle;
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
        # meishi with a frame.  The margin outside the frame is
        # intended to be cut off after printing the meishis.
        if True: #self._debug > 0:
            e.addRect(
                width        = width, 
                height       = height,
                stroke       = 'gray',
                stroke_width = 0.1,
                fill         = 'none'
            )

        # Calculate position of QR-Code
        qr_x = (width  - qrcode_size) / 2
        qr_y = (height - qrcode_size) / 2
            
        print(">>>>>>>>>>>>> qr_x: {}, qr_y: {}".format(qr_x, qr_y))

        # >>>>>>>>>>>>> rx: 20.640350877192983, ry: 4.5476190476190474
        # >>>>>>>>>>>>> size_x: 43.719298245614034, size_y: 45.904761904761905


        e = e.addTranslate(x=qr_x, y=qr_y)

        print(">>>>>>>>>>>>> qrcode_size: {}".format(qrcode_size))
        
        # Add a white background for the QR-Code
        rect = e.addRect(
            width  = qrcode_size, 
            height = qrcode_size,
            fill   = 'white'
        )
        
        # When the background is white or transparent a frame will be
        # added around the white background for the QR-Code
        if background == None \
           or background == 'none' \
           or background == 'white':
            rect = e.addRect(
                width        = qrcode_size,
                height       = qrcode_size,
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
            width  = qrcode_size,
            height = qrcode_size,
        )

        return plugin

## =========================================================
## =========================================================

## fin
