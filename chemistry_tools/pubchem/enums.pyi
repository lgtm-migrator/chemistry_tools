#!/usr/bin/env python3
#
#  enums.pyi
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
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

# stdlib
from typing import Any

# this package
from enum_tools import IntEnum, StrEnum


class PubChemNamespace(StrEnum):
	CID = Cid = cid = "cid"
	Name = NAME = name = "name"
	SMILES = Smiles = smiles = "smiles"
	INCHIKEY = Inchikey = inchikey = "inchikey"

	def __new__(cls, value, doc): ...

	@classmethod
	def is_valid_value(cls, value: Any) -> bool: ...


# @document_enum
class PubChemFormats(StrEnum):
	"""
	Enum of supported formats for the PubChem REST API.
	"""

	JSON = Json = json = "JSON"
	XML = Xml = xml = "XML"
	CSV = csv = Csv = "CSV"
	PNG = png = Png = "PNG"

	def __new__(cls, value): ...

	@classmethod
	def is_valid_value(cls, value: Any) -> bool: ...


class CoordinateType(IntEnum):
	TWO_D = 1
	THREE_D = 2
	SUBMITTED = 3
	EXPERIMENTAL = 4
	COMPUTED = 5
	STANDARDIZED = 6
	AUGMENTED = 7
	ALIGNED = 8
	COMPACT = 9
	UNITS_ANGSTROMS = 10
	UNITS_NANOMETERS = 11
	UNITS_PIXEL = 12
	UNITS_POINTS = 13
	UNITS_STDBONDS = 14
	UNITS_UNKNOWN = 255

	@classmethod
	def is_valid_value(cls, value: Any) -> bool: ...
