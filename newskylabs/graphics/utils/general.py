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

"""newskylabs/graphics/utils/general.py:

General utility functionality.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/23"

import os, re
from subprocess import Popen

## =========================================================
## Utilities
## ---------------------------------------------------------

def get_package_dir():
    """Get the absolute path of a package local file."""

    script_path = os.path.abspath(__file__)
    scripts_dir = os.path.dirname(os.path.dirname(script_path))
    package_dir = os.path.dirname(os.path.dirname(script_path))
    return package_dir

## =========================================================
## Utilities
## ---------------------------------------------------------

def camelToHyphen(s):
    return re.sub(r'([A-Z])', 
                  lambda match: '-{}'.format(match.group(1).lower()), 
                  s)

def formatKwargsKey(key):
    """
    'fooBar_baz' -> 'foo-bar-baz'
    """
    key = re.sub(r'_', '-', key)
    return key

def formatKwargsValue(value):

    if value == None:
        value = 'none'

    elif isinstance(value, (int, float)):
        value = str(value)

    return value

def formatKwargs(kwargs):
    return {formatKwargsKey(key): formatKwargsValue(value) for key, value in kwargs.items()}

## =========================================================
## Utilities
## ---------------------------------------------------------

def open_file(filepath, application=None):
    """
    Example:
    open_file("some/path/imabe.svg", application='Google Chrome')
    """

    # Get the absolute path of the file to open
    realpath = os.path.realpath(filepath)

    # Assemble command
    cmd = ['open']
    if application:
        cmd += ['-a', application]
    cmd.append(realpath)

    # Print command
    print(' '.join(cmd))

    # Execute command
    p = Popen(cmd)

## =========================================================
## =========================================================

## fin.
