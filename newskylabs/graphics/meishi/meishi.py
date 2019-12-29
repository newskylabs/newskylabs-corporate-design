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

"""newskylabs/graphics/meishi/meishi.py:

The main file with the functionality to render meishis (name cards).

TODO: Put more of the functionality into plugins to allow for a better
parametrization of name cards - and therefore a larger amount of
different designs.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/29"

import os, io, yaml, pprint

# svg -> pdf
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# Merge pdfs
from PyPDF2 import PdfFileMerger

from newskylabs.graphics.svg.svg import SVGElement
from newskylabs.graphics.utils.general import open_file

## =========================================================
## Meishi
## ---------------------------------------------------------

class Meishi:

    _default_data_file = 'default-design.yaml'

    _debug = {
        # 'level':   1,
        'level':   0,
        'margin': 20,
    }

    _content = {

        'name': {
            'family': 'Family',
            'given':  'Name',
            'suffix': 'Jr.',
        },
        
        'title': 'Job Title',
        
        'org': {
            'name': 'Organization Name', 
            'unit': 'Organization Unit',
        },
        
        'contact': {
            'work': {
                'email': 'email@some.where',
                'url':   'https://home.page',
                'tel':   '+12-345-67-89-10',
                'adr': {
                    'street':  'Street 123',
                    'city':    'City',
                    'code':    '12345',
                    'country': 'Country',
                },
            },
        },
    }
    
    _svgfile = {
        'front':  'meishi-front.svg',
        'back':   'meishi-back.svg',
    }
    
    _pdffile = {
        'front':  'meishi-front.pdf',
        'back':   'meishi-back.pdf',
        'merged': 'meishi.pdf',
    }
    
    _color      = 'green'
    _background = 'white'
    
    _parameter = {
        'width':       85,
        'height':      55,
        'margin':      1,
        'color':       _color,
        'background':  'white',
    }
    
    _icon = {
        'class': 'newskylabs.graphics.svg.library.svgicon.SVGIcon',
        'debug':        1,
        'tag':          'rect',
        'x':            0,
        'y':            0,
        'width':        14,
        'height':       14,
        'fill':         _color,
    }
    
    _back_side = {
        'class': 'newskylabs.graphics.svg.library.simplebackside.SimpleBackside',
        'debug':       _debug,
        'parameter':   _parameter,
        'content':     _content,
        'color':       _background,
        'background':  _color,
        'qrcode_size': 45,
    }
    
    _default_data = {
        'debug':             _debug,
        'content':           _content,
        'svgfile':           _svgfile,
        'pdffile':           _pdffile,
        'color':             _color,
        'background':        _background,
        'parameter':         _parameter,
        'icon':              _icon,
        'back-side':         _back_side,
        'default-data-file': _default_data_file,
    }
    
    def __init__(self, datafile=None, debug=0):

        # State
        self._debug = debug
        self._svg_front = None
        self._svg_back = None
        self._saved_front_as = None
        self._saved_back_as = None

        # Initialize the meishi data
        self.init_data(datafile)

    def init_data(self, datafile):

        # Has a 'datafile' been given?
        if datafile \
           and isinstance(datafile, io.TextIOWrapper):
            # When 'datafile' is a stream, 
            # try to read the meishi data from it.
            data = yaml.load(datafile, Loader=yaml.FullLoader)
            
        elif datafile \
             and isinstance(datafile, str) \
             and os.path.isfile(datafile):
            # When 'datafile' is a string, 
            # interpret it as a filepath,
            # open it and try to read the meishi data.
            with open(datafile) as fh:
                data = yaml.load(fh, Loader=yaml.FullLoader)
                
        elif self._default_data_file \
             and os.path.isfile(self._default_data_file):
            # When no data has been given 
            # but the default data file exists
            # use it to read the meishi data
            with open(self._default_data_file) as fh:
                data = yaml.load(fh, Loader=yaml.FullLoader)

        else:
            # When no data has been given 
            # and the default data file does not exist
            # use the default data
            data = self._default_data

        self._data = data

        # DEBUG
        if self._debug > 0:
            print("DEBUG data:")
            print("---")
            pprint.pprint(data)
            print("---")

    def get_data(self, keychain):
        """Get data recursively by keychain:

        self.get_data('some.key.chain')
        <= self._data['some']['key']['chain']

        """
        keychain = keychain.split('.')
        value = self._data
        for key in keychain:
            value = value[key]
        return value

    def generate(self):
        self.generate_front()
        self.generate_back()

    def generate_front(self):

        width       = self.get_data('parameter.width')
        height      = self.get_data('parameter.height')
        margin      = self.get_data('parameter.margin')
        color       = self.get_data('parameter.color')
        background  = self.get_data('parameter.background')

        debug       = self.get_data('debug.level')
        if debug > 0:
            margin = self.get_data('debug.margin')

        # DEBUG
        if debug > 0:
            print("DEBUG Parameters:")
            print("  - debug level: {}".format(debug))
            print("  - width:       {}".format(width))
            print("  - height:      {}".format(height))
            print("  - margin:      {}  (depends on debug level)".format(margin))
            print("  - color:       {}".format(color))
            print("  - background:  {}".format(background))
            print("")

            
        # Get content
        name_family      = self.get_data('content.name.family')
        name_given       = self.get_data('content.name.given')
        name_suffix      = self.get_data('content.name.suffix')
        title            = self.get_data('content.title')
        org_name         = self.get_data('content.org.name')
        org_unit         = self.get_data('content.org.unit')
        work_email       = self.get_data('content.contact.work.email')
        work_url         = self.get_data('content.contact.work.url')
        work_tel         = self.get_data('content.contact.work.tel')
        work_adr_street  = self.get_data('content.contact.work.adr.street')
        work_adr_city    = self.get_data('content.contact.work.adr.city')
        work_adr_code    = self.get_data('content.contact.work.adr.code')
        work_adr_country = self.get_data('content.contact.work.adr.country')
        
        # DEBUG
        if debug > 0:
            print("DEBUG Meishi content:")
            print("  - name_family:      {}".format(name_family))
            print("  - name_given:       {}".format(name_given))
            print("  - name_suffix:      {}".format(name_suffix))
            print("  - title:            {}".format(title))
            print("  - org_name:         {}".format(org_name))
            print("  - org_unit:         {}".format(org_unit))
            print("  - work_email:       {}".format(work_email))
            print("  - work_url:         {}".format(work_url))
            print("  - work_tel:         {}".format(work_tel))
            print("  - work_adr_street:  {}".format(work_adr_street))
            print("  - work_adr_city:    {}".format(work_adr_city))
            print("  - work_adr_code:    {}".format(work_adr_code))
            print("  - work_adr_country: {}".format(work_adr_country))
            print("")

        # Font family:
        #| font_family = '"Gill Sans", sans-serif'
        #| font_family = '"Helvetica Neue", sans-serif';
        #| font_family = '"Avenir Next"';
        font_family = "'Helvetica Neue'";
        font_weight = 200
        font_style  = 'normal'
        gray_font   = '#666'

        # Font sizes:
        header_font_size = '5.16px'
        about_font_size  = '3.41px'
        # For some reason the fonts are sized differently on SVGs and pdfs:
        # Font size for SVG
        #| name_font_size   = '6.0px'
        #| role_font_size   = '3.71px'
        # Font size for pdf
        name_font_size   = '5.75px'
        role_font_size   = '3.56px'
        body_font_size   = about_font_size

        margin_vertical = 4.5
        y = height - margin_vertical
        lh = 5.0 # 5.5
        yb1 = y - 2 * lh
        yb2 = y - 1 * lh
        yb3 = y
    
        margin_horizontal = 4.5
        xl =         margin_horizontal
        xr = width - margin_horizontal
    
        # Calculate the size of the SVG
        svg_width  = width  + 2 * margin
        svg_height = height + 2 * margin
    
        # The root element of the front side
        root = SVGElement.root(width=svg_width, height=svg_height, absolute=True)

        # Add a margin
        e = root.addTranslate(x=margin, y=margin)
    
        # When in DEBUG mode:
        # A rectangle to visualize the size of the meishi
        if debug > 0:
            e.addRect(
                width=85, 
                height=55,
                stroke='gray',
                stroke_width=0.2,
                fill='none'
            )
    
        # ==================
        # Style CSS section
        # ------------------
        style = e.addStyle()
        
        style.addCSSRule(
            '.header',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = header_font_size,
            fill        = gray_font
        )
        
        style.addCSSRule(
            '.about',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = about_font_size,
            fill        = gray_font
        )
          
        style.addCSSRule(
            '.name',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = name_font_size,
            fill        = color,
            text_anchor = 'end'
        )
        
        style.addCSSRule(
            '.role',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = role_font_size,
            fill        = gray_font,
            text_anchor = 'end'
        )
              
        style.addCSSRule(
            '.body-left',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = body_font_size,
            fill        = gray_font
        )
              
        style.addCSSRule(
            '.body-right',
            font_family = font_family,
            font_weight = font_weight,
            font_style  = font_style,
            font_size   = body_font_size,
            fill        = gray_font,
            text_anchor = 'end'
        )
        
        # ==================
        # Add the Icon
        # ------------------
        # Position the icon
        x = margin_horizontal
        y = margin_vertical
        gicon = e.addTranslate(x, y)
        
        # Add the icon graphics
        if 'icon' in self._data:

            # Take icon class and parameters from the settings
            # and render the icon
            icon = self.get_data('icon')
            gicon.addPlugin(icon)
            
        else:

            # No icon given in the settings
            # use the default icon:
            icon = {
                'class':  'newskylabs.graphics.svg.library.svgicon.SVGIcon',
                'tag':    'rect',
                'x':      0, 
                'y':      0, 
                'width':  14,
                'height': 14,
                'fill':   'red', 
            }
            gicon.addPlugin(icon)

        # ==================================================
        # Fill out the meishi 
        # with the personal information of its future owner
        # --------------------------------------------------

        # Organization Name
        e.addText(x=21, y=11, className='header').text(org_name)
        
        # Organization Unit
        e.addText(x=21.15, y=15, className='about').text(org_unit)

        # GivenName FamilyName [, PhD / Jr / ...]
        # When the suffix starts with ', ', the suffix is separated 
        # from the name with a comma o the front side of the meishi:
        # Example: Some Name, Phd
        # A suffix without leading comma like 'Jr.' is rendered 
        # without comma:
        # Example: Some Name Jr.
        # Note that the comma is ignored in the QR-Code o the back side.
        name = '{} {}'.format(name_given, name_family)
        if name_suffix:
            # Does the suffix start with a blank or ', '?
            if name_suffix[0] == ',':
                name += name_suffix
            else:
                name += ' ' + name_suffix
        e.addText(x=xr, y=26.5, className='name').text(name)
    
        # Job Title
        e.addText(x=xr, y=31, className='role').text(title)
    
        # Street 123
        e.addText(x=xl, y=yb1, className='body-left').text(work_adr_street)
        
        # Country Code + City
        city = '{} {}'.format(work_adr_code, work_adr_city)
        e.addText(x=xl, y=yb2, className='body-left').text(city)
    
        # Country
        e.addText(x=xl, y=yb3, className='body-left').text(work_adr_country)
        
        # Telephone number (ex: +12-345-67-89-10)
        e.addText(x=xr, y=yb1, className='body-right').text(work_tel)
    
        # Email (ex: email@some.where)
        e.addText(x=xr, y=yb2, className='body-right').text(work_email)
        
        # URL of homepage (ex: https://home.page)
        e.addText(x=xr, y=yb3, className='body-right').text(work_url)
        
        # Save the SVG code of the front side
        self._svg_front = root
    
    def generate_back(self):
        
        debug  = self.get_data('debug.level')
        width  = self.get_data('parameter.width')
        height = self.get_data('parameter.height')
        margin = self.get_data('parameter.margin')

        if debug > 0:
            margin = self.get_data('debug.margin')

        x = margin
        y = margin

        # DEBUG
        if debug > 0:
            print("DEBUG Parameters:")
            print("  - debug level: {}".format(debug))
            print("  - x:           {}".format(x))
            print("  - y:           {}".format(y))
            print("  - width:       {}".format(width))
            print("  - height:      {}".format(height))
            print("  - margin:      {}  (depends on debug level)".format(margin))
 
        # SVG root element of the back side
        back_side = SVGElement.root(
            width    = width  + 2 * margin, 
            height   = height + 2 * margin, 
            absolute = True
        )
        
        # The design of the back side is specified with a back-side plugin:
        # Add back side plugin
        back_side_plugin = self.get_data('back-side')
        back_side.addPlugin(
            back_side_plugin, 
            x      = x,
            y      = y,
            width  = width, 
            height = height
        )

        # Save the SVG code of the back side
        self._svg_back = back_side
    
    def print(self, side='front'):
        """Print SVG code to stdout."""
        
        if side == 'front':
            self.print_front()
            
        else: # side == 'back'
            self.print_back()

    def print_front(self):
        """Print SVG code to stdout."""
        
        # Ensure that the svg has been generated
        if not self._svg_front:
            self.generate_front()
            
        self._svg_front.print()

    def print_back(self):
        """Print SVG code to stdout."""
        
        # Ensure that the svg has been generated
        if not self._svg_back:
            self.generate_back()
            
        self._svg_back.print()
    
    def save(self, front=True, back=True, show=True, pdf=True, merge=True):

        frontfile = self.save_front(front=front, show=show, pdf=pdf)
        backfile  = self.save_back(back=back, show=show, pdf=pdf)

        # whould I merge the front and back pdfs into one pdf?
        if front and back and pdf and merge:

            # Is 'merge' a string?
            # If so use it as pdf file name
            if isinstance(merge, str):
                mergedfile = pdf

            else: # Interpreted as True
                mergedfile = self.get_data('pdffile.merged')

            # Print a message
            print("Saving front and back side combined as {}".format(mergedfile))

            pdfs = [frontfile, backfile]

            merger = PdfFileMerger()

            for pdf in pdfs:
                merger.append(pdf)
            
            merger.write(mergedfile)
            merger.close()

            # Should I show the generated pdf?
            if show:
                open_file(mergedfile)
    
            return mergedfile

        return frontfile, backfile
        
    def save_front(self, front=None, show=False, pdf=True):
        
        # Ensure that the svg has been generated
        if not self._svg_front:
            self.generate_front()

        # When no svgfile has been given
        # take it from the data
        if isinstance(front, str):
            svgfile = front

        else:
            svgfile = self.get_data('svgfile.front')

        # Print a message
        print("Saving front side of meishi as {}".format(svgfile))

        # Save as SVG file
        self._svg_front.save(svgfile)

        # Should I show the generated SVG?
        if show:
            application = 'Google Chrome'
            open_file(svgfile, application=application)
    
        # Remember last file saved to
        self._saved_front_as = svgfile

        # Save as pdf?
        if pdf:

            # Is 'pdf' a string?
            # If so use it as pdf file name
            if isinstance(pdf, str):
                pdffile = pdf

            else:
                pdffile = self.get_data('pdffile.front')

            # Print a message
            print("Saving front side of meishi as {}".format(pdffile))

            # Convert saved svg to pdf
            self.svg2pdf(svgfile, pdffile)

            # Return svg and pdf file name
            return pdffile

        # Default - do not save as pdf
        # Return svg file name
        return svgfile

    def save_back(self, back=None, show=False, pdf=True):
        
        # Ensure that the svg has been generated
        if not self._svg_back:
            self.generate_back()

        # When no svgfile has been given
        # take it from the data
        if isinstance(back, str):
            svgfile = back

        else:
            svgfile = self.get_data('svgfile.back')

        # Print a message
        print("Saving back side of meishi as {}".format(svgfile))

        # Save as SVG file
        self._svg_back.save(svgfile)

        # Should I show the generated SVG?
        if show:
            application = 'Google Chrome'
            open_file(svgfile, application=application)
    
        # Remember last file saved to
        self._saved_back_as = svgfile

        # Save as pdf?
        if pdf:

            # Is 'pdf' a string?
            # If so use it as pdf file name
            if isinstance(pdf, str):
                pdffile = pdf

            else:
                pdffile = self.get_data('pdffile.back')

            # Print a message
            print("Saving back side of meishi as {}".format(pdffile))

            # Convert saved svg to pdf
            self.svg2pdf(svgfile, pdffile)

            # Return svg and pdf file name
            return pdffile

        # Default - do not save as pdf
        # Return svg file name
        return svgfile

    def svg2pdf(self, svgfile, pdffile):
        """Convert SVG to pdf"""

        drawing = svg2rlg(svgfile)
        renderPDF.drawToFile(drawing, pdffile)

    def show(self, side='front'):

        if side == 'front':
            self.show_front()

        else: # side == 'back'
            self.show_back()

    def show_front(self, application='Google Chrome'):

        # Ensure that the svg has been generated
        if not self._saved_front_as:
            self.save_front()

        # Get the filename
        filename = self._saved_front_as

        # Open the SVG file
        open_file(filepath, application=application)

    def show_back(self, application='Google Chrome'):

        # Ensure that the svg has been generated
        if not self._saved_back_as:
            self.save_back()

        # Get the filename
        filename = self._saved_back_as

        # Open the SVG file
        open_file(filepath, application=application)

## =========================================================
## =========================================================

## fin
