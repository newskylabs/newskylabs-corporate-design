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

"""newskylabs/graphics/xml/xml.py:

A class wrapping lxml.etree.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/12"

import os
from lxml import etree
from newskylabs.graphics.utils.general import formatKwargs

## =========================================================
## class XMLElement 
## 
## A wrapper for lxml.etree
## ---------------------------------------------------------

class XMLElement():
    """
    XMLElement - a class wrapping lxml.etree.
    """

    _namespace = None
    _root_tag = 'xml'

    def __init__(self, tag, *args, **kwargs):
        tag = etree.QName(self._namespace, tag)
        kwargs = formatKwargs(kwargs)
        xml = etree.Element(tag, *args, **kwargs)
        self._xml = xml

    @classmethod
    def root(cls, *args, **kwargs):
        tag = cls._root_tag
        if cls._namespace:
            nsmap = {None : cls._namespace}
            kwargs['nsmap'] = nsmap
        root = cls(tag, *args, **kwargs)
        return root

    def append(self, element):

        if isinstance(element, self.__class__):
            # ELEMENT is an XMLElement
            # Append the element and return it
            element = element._xml

        elif isinstance(element, etree._Element):
            # ELEMENT is an etree.Element
            # Append the element and return the current element
            # element = element
            pass

        else:
            # ELEMENT is neither an XMLElement nor an etree.Element
            # Throw an error
            msg = "Argument 'element' has incorrect type " \
                + "(expected either an lxml.etree._Element or an XMLElement, " \
                + ", got {}".format(type(element))
            raise TypeError(msg)

        self._xml.append(element)
        return element

    def text(self, text):
        self._xml.text = text
        return self

    def depth(self):
        """Returns number of parents"""
        return sum(1 for _ in self._xml.iterancestors())

    def tostring(self, pretty_print=True, xml_declaration=True, encoding='utf-8'):

        string = etree.tostring(
            self._xml, 
            pretty_print    = pretty_print,
            xml_declaration = xml_declaration, 
            encoding        = encoding,
        ).decode(encoding)

        return string

    def print(self, pretty_print=True, xml_declaration=True, encoding='utf-8'):

        string = self.tostring(
            pretty_print    = pretty_print, 
            xml_declaration = xml_declaration, 
            encoding        = encoding
        )

        print(string)

    def save(self, filename, 
             pretty_print=True, xml_declaration=True, encoding='utf-8'):

        string = self.tostring(
            pretty_print    = pretty_print, 
            xml_declaration = xml_declaration, 
            encoding        = encoding
        )

        with open(filename, 'w') as stream:
            stream.write(string)

## =========================================================
## =========================================================

## fin.
