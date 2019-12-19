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

"""examples/newskylabs/graphics/svg/library/vcard_examples.py:

VCard usage examples.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/19"

import os
import sys
import tempfile

from newskylabs.graphics.utils.examples import main

from examples.newskylabs.graphics.svg.library.vcard_example_data import get_example_data
from newskylabs.graphics.svg.library.vcard import VCard

## =========================================================
## Examples
## ---------------------------------------------------------

def vcard_example_print():
    data = get_example_data(ex=0)
    vc = VCard(data)
    vc.print()

def vcard_example_print_raw():
    data = get_example_data(ex=0)
    vc = VCard(data)
    vc.print(raw=True)

def vcard_example_pretty_print():
    data = get_example_data(ex=0)
    vc = VCard(data)
    vc.pretty_print()

def vcard_example_to_QRCode_png():
    data = get_example_data(ex=0)
    vc = VCard(data)
    qr_code = vc.to_QRCode()
    qr_code_img = qr_code.to_img()
    qr_code_file = '/tmp/qr-code.png'
    qr_code_img.save(qr_code_file)
    from newskylabs.graphics.utils.general import open_file
    open_file(qr_code_file)

def vcard_example_to_QRCode_jpg():
    data = get_example_data(ex=0)
    vc = VCard(data)
    qr_code = vc.to_QRCode()
    qr_code_img = qr_code.to_img()
    qr_code_file = '/tmp/qr-code.jpg'
    qr_code_img.save(qr_code_file)
    from newskylabs.graphics.utils.general import open_file
    open_file(qr_code_file)

## =========================================================
## Main
## ---------------------------------------------------------

if __name__ == '__main__':
    main(globals())

## =========================================================
## =========================================================

## fin.
