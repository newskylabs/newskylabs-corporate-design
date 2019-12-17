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

"""newskylabs/graphics/svg/library/vcard.py:

Class VCard

A wrapper for vobject.vCard.

See: 

  - VObject
    A full-featured Python package for parsing and creating iCalendar
    and vCard files
    https://eventable.github.io/vobject

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/17"

import vobject
import re

## =========================================================
## class VCard
## 
## A wrapper for vobject.vCard
## ---------------------------------------------------------

class VCard:
    """
    A wrapper for vobject.vCard.
    """

    def __init__(self, data):

        # DEBUG
        #| print("DEBUG VCard data: {}".format(data))

        vcard = vobject.vCard()
        self._vcard = vcard

        j = vobject.vCard()

        # Name: name / given / family
        name = data['name']
        given  = name['given']
        family = name['family']
        suffix = name['suffix']

        # Render suffix with or without comma?
        # Examples:
        # - with comma:    'Given Name, PhD'
        # - without comma: 'Given Name Jr.'
        with_comma = suffix[0] == ','
        suffix = re.sub('^, *', '', suffix)
        
        # Add name
        vcard.add('n')
        vcard.n.value = vobject.vcard.Name( 
            family = family,
            given  = given,
            suffix = suffix
        )

        # Add fn
        vcard.add('fn')
        if 'fn' in name:
            vcard.fn.value = name['fn']
        else:
            if with_comma:
                vcard.fn.value = '{} {}, {}'.format(given, family, suffix)
            else:
                vcard.fn.value = '{} {} {}'.format(given, family, suffix)

        # Add title
        vcard.add('title')
        vcard.title.value = data['title']

        # Add org
        org = data['org']
        vcard.add('org')
        vcard.org.value = [
            org['name'],
            org['unit']
        ]

        # Add tel
        contact = data['contact']
        work = contact['work']
        #| home = contact['home']
        vcard.add('tel')
        vcard.tel.type_param = ['WORK', 'VOICE']
        vcard.tel.value = work['tel']

        # Add adr
        adr = work['adr']
        vcard.add('adr')
        vcard.adr.type_param = 'WORK'
        vcard.adr.value = vobject.vcard.Address(
            street  = adr['street'],
            city    = adr['city'],
            code    = adr['code'],
            country = adr['country']
        )

        # Add email
        vcard.add('email')
        vcard.email.type_param = 'INTERNET'
        vcard.email.value = work['email']

        # Add url
        vcard.add('url')
        vcard.url.value = work['url']

        # Convert to string
        vcardStr = vcard.serialize()

    def serialize(self):

        # Convert to string
        vcard_str = self._vcard.serialize()
        return vcard_str

    def print(self, raw=False):

        if raw:
            print(repr(self.serialize()))
        else:
            print(self.serialize())

    def pretty_print(self):

        vcard = self._vcard.prettyPrint()

## =========================================================
## =========================================================

## fin.
