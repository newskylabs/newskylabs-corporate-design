"""newskylabs/graphics/scripts/meishi.py:

Entry point of the `nsl-meishi` command.

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2019/12/12"

import click

## =========================================================
## Command: nsl-meishi
## ---------------------------------------------------------

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('datafile', type=click.File('r'), required=False)
def meishi(datafile):
    """A program to generate meishis (name cards).

Rather than using the default data, a yaml DATAFILE can be specified
on the command line containing the personal information and design
parameters which should be used to generate the meishi.
    """
    print('Hello World :)')
    print('DEBUG datafile: {}'.format(datafile))

## =========================================================
## Main
## ---------------------------------------------------------
 
if __name__ == '__main__':
    meishi()

## =========================================================
## =========================================================

## fin.
