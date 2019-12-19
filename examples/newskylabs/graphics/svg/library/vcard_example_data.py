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

"""examples/newskylabs/graphics/svg/library/vcard_example_data.py:

Data for VCard examples.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/19"

## =========================================================
## Data for VCard examples
## ---------------------------------------------------------

_data0 = {
    
    'name': {
        'family': 'Family',
        'given':  'Name',
        # 'suffix': ',PhD',
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
        'home': None,
    }
}

_data = [
    _data0,
]

## =========================================================
## get_example_data()
## ---------------------------------------------------------

def get_example_data(ex=0):
    return _data[ex]

## =========================================================
## =========================================================

## fin.
