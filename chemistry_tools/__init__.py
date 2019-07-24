#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright (c) 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Assay, Atom, Bond, Compound, Constants, Errors, Lookup, Substance and
#  Utils based on PubChemPy by Matt Swain <m.swain@me.com>
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

__author__ = "Dominic Davis-Foster"
__copyright__ = "2019 Dominic Davis-Foster"

__license__ = "LGPL"
__version__ = "0.1.2"
__email__ = "dominic@davis-foster.co.uk"

__all__ = ["SpectrumSimilarity", "Assay", "Atom", "Bond", "Compound", "Constants", "Errors", "PropertyFormat",
		   "Substance", "Toxnet", "Utils"]

import requests_cache

requests_cache.install_cache(expire_after=3600)


from . import Assay
from . import Atom
from . import Bond
from . import Compound
from . import Constants
from . import Errors
from . import Lookup
from . import PropertyFormat
from . import SpectrumSimilarity
from . import Substance
from . import Toxnet
from . import Utils

if __name__ == '__main__':
	print(__version__)

