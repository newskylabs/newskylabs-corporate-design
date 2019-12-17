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

"""newskylabs/graphics/utils/examples.py:

Utilities for running the examples in the 'examples' dir.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/17"

import os
import sys
from inspect import isfunction

## =========================================================
## Utilities
## ---------------------------------------------------------

def get_example_prefix():
    """Calculate the prefix of the example functions
    
    Example: 
    
      'some-class-examples' -> 'some_class_example_'

    """

    # Get the name of the examples script
    script_name = os.path.basename(sys.argv[0])
    example_prefix = script_name

    # Get rid of the final 's'
    # Example: 'some-class-examples' -> 'some-class-example'
    example_prefix = example_prefix[:-1]

    # Substitute '_' for '-'
    # Example: 'some-class-example' -> 'some_class_example'
    example_prefix = example_prefix.replace('-', '_')

    # Append a final '_'
    # Example: 'some_class_example' -> 'some_class_example_'
    example_prefix += '_'

    return example_prefix

def get_examples(symbols):

    # Calc length of example prefix
    example_prefix = get_example_prefix()
    example_prefix_length = len(example_prefix)

    # Get all functions starting with 'example_prefix'
    examples = {n: f for n, f in symbols.items() 
                if isfunction(f) 
                and n[:example_prefix_length] == example_prefix}

    return examples

## =========================================================
## usage()
## ---------------------------------------------------------

def usage(examples):

    # Get the path of the examples script
    script_path = sys.argv[0]

    # Get the name of the examples script
    script_name = os.path.basename(sys.argv[0])

    print("Usage:")
    print("")
    print("alias {}=\"{}\"".format(script_name, script_path))
    print("")
    for example in examples:
        print("{} {}".format(script_name, example))
    print("")

## =========================================================
## main()
## ---------------------------------------------------------

def main(symbols):

    # Get example functions
    examples = get_examples(symbols)

    # Exactly one example should have been given
    # as parameter on the command line
    if len(sys.argv) != 2:
        usage(examples)
        exit()

    # The example given as parameter on the command line should exist
    example = sys.argv[1]
    if not example in examples:
        usage(examples)
        exit()

    # Call the example...
    print("")
    print(">>> {}()".format(example))
    print("")
    examples[example]()

## =========================================================
## =========================================================

## fin.
