#!/usr/bin/env python
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

"""examples/newskylabs/graphics/svg/library/qrcode_examples.py:

QRCode usage examples.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/21"

from newskylabs.graphics.utils.examples import main

from examples.newskylabs.graphics.svg.library.vcard_example_data import get_example_data
from newskylabs.graphics.utils.general import open_file

from newskylabs.graphics.svg.library.qrcode import QRCode

## =========================================================
## Examples
## ---------------------------------------------------------

def qrcode_example_print_example_data():
    data = get_example_data(ex=0)
    print(data)

def qrcode_example_to_img():
    data = get_example_data(ex=0)
    qrcode = QRCode(data)
    img = qrcode.to_img()
    img.show()

def qrcode_save_and_show(itype='png'):
    data = get_example_data(ex=0)
    qrcode = QRCode(data)
    img = qrcode.to_img()
    filename = '/tmp/qr-code.{}'.format(itype)
    img.save(filename)
    open_file(filename)

def qrcode_example_to_png():
    qrcode_save_and_show(itype='png')

def qrcode_example_to_jpg():
    qrcode_save_and_show(itype='jpg')

def qrcode_to_svg(method=None):
    data = get_example_data(ex=0)
    qrcode = QRCode(data)
    img = qrcode.to_img(itype='svg', method=method)
    if method == None: 
        img.show()
        
    else:
        # The methods 'basic', 'fragment', and 'path'
        # do not have a 'show()' method:
        import tempfile
        _, filename = tempfile.mkstemp(suffix='.svg', prefix='qrcode.', dir='/tmp', text=True)
        img.save(filename)
        application = 'Google Chrome'
        open_file(filename, application=application)

def qrcode_example_to_svg():
    qrcode_to_svg()

def qrcode_example_to_svg_basic(method='basic'):
    qrcode_to_svg(method=method)

def qrcode_example_to_svg_fragment(method='fragment'):
    qrcode_to_svg(method=method)

def qrcode_example_to_svg_path(method='path'):
    qrcode_to_svg(method=method)

def qrcode_example_to_SVGElement():

    # The dimensions of the QR-Code
    width, height = 100, 100

    # Make an SVG root element
    from newskylabs.graphics.svg.svg import SVGElement
    root = SVGElement.root(width=width, height=height, absolute=True)

    # Make an QR-Code SVG element
    data = get_example_data(ex=0)
    qrcode = QRCode(data)
    qrcode_svg_element = qrcode.to_SVGElement(
        x      = 0,
        y      = 0,
        width  = width,
        height = height
    )

    # Append the QR-Code SVG element to the SVG root element
    root.append(qrcode_svg_element)

    # Get a temporary file name
    import tempfile
    _, svgfile = tempfile.mkstemp(suffix='.svg', prefix='qrcode.', dir='/tmp', text=True)

    # Save the SVG file
    root.save(svgfile)

    # And finally open it
    application = 'Google Chrome'
    open_file(svgfile, application=application)

## =========================================================
## Main
## ---------------------------------------------------------

if __name__ == '__main__':
    main(globals())

## =========================================================
## =========================================================

## fin.
