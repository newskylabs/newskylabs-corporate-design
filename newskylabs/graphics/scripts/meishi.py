"""newskylabs/graphics/scripts/meishi.py:

Entry point of the `nsl-meishi` command.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/31"

import click
import os

from newskylabs.graphics.meishi import Meishi
from newskylabs.graphics.utils.general import get_package_dir

## =========================================================
## Utilities
## ---------------------------------------------------------

def get_default_design():
    """Get the parameters defining the default design for meishis (name
    cards).

    """
    package_dir = get_package_dir()
    defaults_file = package_dir + '/meishi/designs/default-design.yaml'
    return defaults_file

## =========================================================
## Command: nsl-meishi
## ---------------------------------------------------------

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('datafile', type=click.File('r'), required=False, default=get_default_design())
def meishi(datafile):
    """A program to generate meishis (name cards).

    Rather than using the default design, a yaml DATAFILE can be
    specified on the command line defining the information to be
    written on the meishi and the design parameters which should be
    used to generate the meishi layout.

    """

    meishi = Meishi(datafile=datafile)
    meishi.generate()

    # DEBUG
    #| meishi.print()
    
    show = True
    meishi.save(show=show)

## =========================================================
## Main
## ---------------------------------------------------------
 
if __name__ == '__main__':
    meishi()

## =========================================================
## =========================================================

## fin.
