#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  __init__.py
"""Lookup properties for chemicals, from PubChem and Toxnet"""
#
#  Copyright (c) 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on PubChemPy by Matt Swain <m.swain@me.com>
#  Available under the MIT License
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


__author__ = 'Matt Swain'
__email__ = 'm.swain@me.com'
__version__ = '0.1.0'
__license__ = 'LGPL'

from .toxnet import toxnet
from .PropertyFormat import *

from .errors import ResponseParseError, PubChemHTTPError, BadRequestError
from .errors import NotFoundError, MethodNotAllowedError, TimeoutError
from .errors import UnimplementedError, ServerError

from .utils import *

from .Compound import Compound, get_compounds, compounds_to_frame
from .Atom import Atom
from .Bond import Bond
from .Assay import Assay, get_assays
from .Substance import Substance, get_substances, substances_to_frame

from .constants import ELEMENTS


if __name__ == '__main__':
	print(__version__)
