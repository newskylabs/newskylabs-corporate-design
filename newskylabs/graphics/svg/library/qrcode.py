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

"""newskylabs/graphics/svg/library/qrcode.py:

QRCode class.

A Class to generate QR-Codes image files and SVG elements from given data.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/21"

import qrcode
import qrcode.image.svg
from lxml import etree

from newskylabs.graphics.svg.svg import SVGElement

## =========================================================
## class QRCode
## ---------------------------------------------------------

class QRCode():

    def __init__(self, data, debug=1):
        self._data  = data
        self._debug = debug

        # DEBUG
        if debug > 0:
            print("DEBUG QRCode data: {}".format(data))

    def get_data(self):
        return self._data

    def to_img(self, itype=None, method=None):

        # Convert string to QR-Code image
        import qrcode
        data = self._data

        if itype == 'svg':

            if method == 'basic':
                # Simple image_factory, just a set of rects.
                image_factory = qrcode.image.svg.SvgImage
        
            elif method == 'fragment':
                # Fragment image_factory (also just a set of rects)
                image_factory = qrcode.image.svg.SvgFragmentImage

            elif method == 'path':
                # Combined path image_factory, 
                # fixes white space that may occur when zooming
                image_factory = qrcode.image.svg.SvgPathImage

            else:
                # SVG Using my SVGElement class
                image_factory = QRSVGImageFactory

            img = qrcode.make(data, image_factory=image_factory)

        else: # itype: png | jpg | ...
            img = qrcode.make(data)

        return img

    def to_SVGElement(self, 
                      x      = 0,
                      y      = 0,
                      width  = 10,
                      height = 10,
                      debug  = 0
    ):
        """
        Convert to an SVGElement.
        """

        # Use a group tag 'g' to add the QR-Code
        svg = SVGElement('g')

        # DEBUG
        debug = self._debug
        if debug > 0:
            print("DEBUG QRCode:")
            print("  - x:      {}".format(x))
            print("  - y:      {}".format(y))
            print("  - width:  {}".format(width))
            print("  - height: {}".format(height))

        # When values vor x and y have been given
        # implement them by translating the QR-Code
        if x != 0 or y != 0:
            svg = svg.addTranslate(x, y)

        # Connection Pattern with QR-Code
        data = self._data

        # Use SVGElement factory
        image_factory_class = QRSVGElementFactory
        qr = qrcode.main.QRCode(image_factory=image_factory_class)
        qr.add_data(data)
        image_factory = qr.make_image()

        # Retrive SVG element
        qrcode_element = image_factory.get_element()

        # Retrive size of SVG element 
        # and convert it from decimal.Decimal to float
        dimension = float(image_factory.get_dimension())
    
        # Scale the QR-Code 
        # to fit into the rectangle defined by width and height
        width  = width  / dimension
        height = height / dimension
        scale  = svg.addScale(width, height)

        # Finally append the QR-Code
        scale.append(qrcode_element)

        # Return the local root element
        return svg

## =========================================================
## =========================================================
## Image Factory classes 
## to generate the QR-Code as SVGElement
## 
## Compare with the corresponding files of the qrcode package: 
## 
##   - qrcode/image/svg.py
##   - qrcode/main.py
##   - qrcode/console_scripts.py
## 
## ---------------------------------------------------------

## =========================================================
## class QRSVGImageFactory
## ---------------------------------------------------------

class QRSVGImageFactory(qrcode.image.svg.SvgPathImage):
    """
    NSL Version of SvgPathImage.

    Compare to class SvgPathImage in site-packages/qrcode/image/svg.py
    """

    _SVG_namespace = 'http://www.w3.org/2000/svg'
    QR_PATH_STYLE = 'fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none'

    def __init__(self, *args, **kwargs):
        self._svg_calculated = False
        super(QRSVGImageFactory, self).__init__(*args, **kwargs)

    def _svg(self, tag=None, version='1.1', viewBox=None, **kwargs):
        
        if viewBox is None:
            dimension = self.units(self.pixel_size, text=False)
            viewBox = '0 0 %(d)s %(d)s' % {'d': dimension}
        
        namespace = self._SVG_namespace
        if tag is None:
            tag = etree.QName(namespace, 'svg') # {http://www.w3.org/2000/svg}svg
        nsmap = {None : namespace} # Default namespace for element and all childs
        dimension = self.units(self.pixel_size)

        svg = etree.Element(
            tag, 
            nsmap=nsmap,
            width=dimension, height=dimension, version=version, viewBox=viewBox,
            **kwargs
        )

        return svg

    def _rect(self, row, col, tag=None):

        if tag is None:
            tag = etree.QName(self._SVG_namespace, 'rect')
        x, y = self.pixel_box(row, col)[0]

        rect = etree.Element(
            tag, 
            x=self.units(x), y=self.units(y),
            width=self.unit_size, height=self.unit_size
        )

        return rect

    def _ensure_svg_calculated(self):
        if not self._svg_calculated:
            self._img.append(self.make_path())
            self._svg_calculated = True

    def to_string(self, pretty_print = True, xml_declaration = True):

        self._ensure_svg_calculated()

        svg = etree.ElementTree(self._img)
        svg_str = etree.tostring(
            svg, 
            pretty_print = True, 
            xml_declaration = True, 
            encoding='UTF-8', 
        ).decode('utf-8')

        return svg_str
        
    def print(self, pretty_print = True, xml_declaration = True):

        svg_str = self.to_string(pretty_print=pretty_print, xml_declaration=xml_declaration)
        print(svg_str)

    def _write(self, stream, pretty_print = True, xml_declaration = True):

        svg_str = self.to_string(pretty_print=pretty_print, xml_declaration=xml_declaration)
        stream.write(svg_str)

    def make_path(self):
        
        subpaths = self._generate_subpaths()

        tag   = etree.QName(self._SVG_namespace, 'path')
        style = self.QR_PATH_STYLE
        d     = ' '.join(subpaths)
        id    = 'qr-path'

        path = etree.Element(tag, style=style, d=d, id=id)

        return path

    def save(self, filename, pretty_print=False, xml_declaration=True):
        with open(filename, 'w') as stream:
          self._write(stream)

    def show(self, filename=None, application='Google Chrome',
             pretty_print=False, xml_declaration=True):

        if not filename:
            import tempfile
            _, filename = tempfile.mkstemp(suffix='.svg', prefix='qrcode.', dir='/tmp', text=True)

        self.save(filename, pretty_print=pretty_print, xml_declaration=xml_declaration)

        from newskylabs.graphics.utils.general import open_file
        open_file(filename, application=application)

        return filename

## =========================================================
## class QRSVGElementFactory
## ---------------------------------------------------------

class QRSVGElementFactory(qrcode.image.svg.SvgPathImage):
    """
    NSL Version of SvgPathImage.

    Compare to class SvgPathImage in site-packages/qrcode/image/svg.py
    """

    _SVG_namespace = 'http://www.w3.org/2000/svg'
    QR_PATH_STYLE = 'fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none'

    def __init__(self, *args, **kwargs):
        self._svg_calculated = False
        super(QRSVGElementFactory, self).__init__(*args, **kwargs)

    def _svg(self, *args, **kwargs):
        
        namespace = self._SVG_namespace
        tag = etree.QName(namespace, 'g') # {http://www.w3.org/2000/svg}g

        svg = etree.Element(tag, *args, **kwargs)

        return svg

    def _rect(self, row, col, tag=None):

        if tag is None:
            tag = etree.QName(self._SVG_namespace, 'rect')
        x, y = self.pixel_box(row, col)[0]

        rect = etree.Element(
            tag, 
            x=self.units(x), y=self.units(y),
            width=self.unit_size, height=self.unit_size
        )

        return rect

    def _ensure_svg_calculated(self):
        if not self._svg_calculated:
            self._img.append(self.make_path())
            self._svg_calculated = True

    def get_element(self):
        self._ensure_svg_calculated()
        return self._img

    def get_dimension(self):
        dimension = self.units(self.pixel_size, text=False)
        return dimension

    def get_viewBox(self):
        dimension = self.units(self.pixel_size, text=False)
        viewBox = '0 0 %(d)s %(d)s' % {'d': dimension}
        return viewBox
        
    def to_string(self, pretty_print = True, xml_declaration = True):

        self._ensure_svg_calculated()

        svg = etree.ElementTree(self._img)
        svg_str = etree.tostring(
            svg, 
            pretty_print = True, 
            xml_declaration = True, 
            encoding='UTF-8', 
        ).decode('utf-8')

        return svg_str
        
    def print(self, pretty_print = True, xml_declaration = True):

        svg_str = self.to_string(pretty_print=pretty_print, xml_declaration=xml_declaration)
        print(svg_str)

    def _write(self, stream, pretty_print = True, xml_declaration = True):

        svg_str = self.to_string(pretty_print=pretty_print, xml_declaration=xml_declaration)
        stream.write(svg_str)

    def make_path(self):
        
        subpaths = self._generate_subpaths()

        tag   = etree.QName(self._SVG_namespace, 'path')
        style = self.QR_PATH_STYLE
        d     = ' '.join(subpaths)
        id    = 'qr-path'

        path = etree.Element(tag, style=style, d=d, id=id)

        return path

    def save(self, filename, pretty_print = True, xml_declaration = True):
        with open(filename, 'w') as stream:
          self._write(stream)

## =========================================================
## =========================================================

## fin
