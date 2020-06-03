#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  elements.py
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
#  Based on molmass (https://github.com/cgohlke/molmass)
#  |  Copyright (c) 1990-2020, Christoph Gohlke
#  |  All rights reserved.
#  |  Licensed under the BSD 3-Clause License
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  1. Redistributions of source code must retain the above copyright notice,
#  |     this list of conditions and the following disclaimer.
#  |
#  |  2. Redistributions in binary form must reproduce the above copyright notice,
#  |     this list of conditions and the following disclaimer in the documentation
#  |     and/or other materials provided with the distribution.
#  |
#  |  3. Neither the name of the copyright holder nor the names of its
#  |     contributors may be used to endorse or promote products derived from
#  |     this software without specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  |  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  |  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  |  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  |  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  |  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  |  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  |  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  |  POSSIBILITY OF SUCH DAMAGE.
#  |
#

# stdlib
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

# this package
from . import _elements, _table
from domdf_python_tools import doctools  # type: ignore # TODO
from domdf_python_tools.bases import Dictable  # type: ignore # TODO
from memoized_property import memoized_property  # type: ignore

IsotopeDict = Dict[int, Union["Isotope", Tuple[float, float]]]


class Element(Dictable):
	"""
	Chemical element.
	"""

	def __init__(
			self,
			number: int,
			symbol: str,
			name: str,
			group: int = 0,
			period: int = 0,
			block: str = '',
			series: int = 0,
			mass: float = 0.0,
			eleneg: float = 0.0,
			eleaffin: float = 0.0,
			covrad: float = 0.0,
			atmrad: float = 0.0,
			vdwrad: float = 0.0,
			tboil: float = 0.0,
			tmelt: float = 0.0,
			density: float = 0.0,
			eleconfig: str = '',
			oxistates: str = '',
			ionenergy: Optional[Tuple] = None,  # TODO
			isotopes: Optional[IsotopeDict] = None,
			description: str = '',
			):

		super().__init__()

		self._number: int = number
		self._symbol: str = symbol
		self._name: str = name
		self._electrons: int = number
		self._protons: int = number
		self._group: int = group
		self._period: int = period
		self._block: str = block
		self._series: int = series
		self._mass: float = mass
		self._eleneg: float = eleneg
		self._eleaffin: float = eleaffin
		self._covrad: float = covrad
		self._atmrad: float = atmrad
		self._vdwrad: float = vdwrad
		self._tboil: float = tboil
		self._tmelt: float = tmelt
		self._density: float = density
		self._eleconfig: str = eleconfig
		self._oxistates: str = oxistates
		self._description: str = description

		if ionenergy is None:
			self._ionenergy = tuple()  # type: ignore # TODO
		else:
			self._ionenergy = ionenergy  # type: ignore # TODO

		self._isotopes: Dict[int, Isotope] = {}

		if isotopes is not None:
			for massnumber, isotope in isotopes.items():
				if isinstance(isotope, Isotope):
					self._isotopes[int(massnumber)] = isotope
				elif isinstance(isotope, (list, tuple)):
					self._isotopes[int(massnumber)] = Isotope(*isotope, massnumber)

	@property
	def __dict__(self):
		return dict(
				number=self._number,
				symbol=self._symbol,
				name=self._name,
				group=self._group,
				period=self._period,
				block=self._block,
				series=self._series,
				mass=self._mass,
				eleneg=self._eleneg,
				eleaffin=self._eleaffin,
				covrad=self._covrad,
				atmrad=self._atmrad,
				vdwrad=self._vdwrad,
				tboil=self._tboil,
				tmelt=self._tmelt,
				density=self._density,
				eleconfig=self._eleconfig,
				oxistates=self._oxistates,
				ionenergy=self._ionenergy,
				isotopes=self._isotopes,
				description=self._description
				)

	@memoized_property
	def number(self) -> int:
		"""
		Returns the atomic number of the element.

		:rtype: int
		"""

		return self._number

	@memoized_property
	def symbol(self) -> str:
		"""
		Returns the chemical symbol of the element.
		"""

		return self._symbol

	@memoized_property
	def name(self) -> str:
		"""
		Returns the name of the element in English.
		"""

		return self._name

	@memoized_property
	def electrons(self) -> int:
		"""
		Returns the number of electrons in the element.

		:rtype: int
		"""

		return self._electrons

	@memoized_property
	def protons(self) -> int:
		"""
		Returns the number of protons in the element.

		:rtype: int
		"""

		return self._protons

	@memoized_property
	def group(self) -> int:
		"""
		Returns the group of the element in the periodic table.

		:rtype: int
		"""

		return self._group

	@memoized_property
	def period(self) -> int:
		"""
		Returns the Period of the element in the periodic table.

		:rtype: int
		"""

		return self._period

	@memoized_property
	def block(self) -> str:
		"""
		Returns the Block of the element in the periodic table.

		:rtype: str
		"""

		return self._block

	@memoized_property
	def series(self) -> int:
		"""
		Index to chemical series.

		:rtype: int
		"""

		return self._series

	@memoized_property
	def mass(self) -> float:
		"""
		Returns the relative atomic mass.

		Ratio of the average mass of atoms.

		:rtype: float
		"""
		return self._mass

	molecular_weight = mass

	@memoized_property
	def eleneg(self) -> float:
		"""
		Returns the Electronegativity (Pauling scale).

		:rtype: float
		"""

		return self._eleneg

	@memoized_property
	def eleaffin(self) -> float:
		"""
		Returns the electron affinity in eV.

		:rtype: float
		"""

		return self._eleaffin

	@memoized_property
	def covrad(self) -> float:
		"""
		Returns the Covalent radius in Angstrom.

		:rtype: float
		"""

		return self._covrad

	@memoized_property
	def atmrad(self) -> float:
		"""
		Returns the Atomic radius in Angstrom.

		:rtype: float
		"""

		return self._atmrad

	@memoized_property
	def vdwrad(self) -> float:
		"""
		Returns the Van der Waals radius in Angstrom.

		:rtype: float
		"""

		return self._vdwrad

	@memoized_property
	def tboil(self) -> float:
		"""
		Returns the boiling temperature in K.

		:rtype: float
		"""

		return self._tboil

	@memoized_property
	def tmelt(self) -> float:
		"""
		Returns the melting temperature in K.

		:rtype: float
		"""

		return self._tmelt

	@memoized_property
	def density(self) -> float:
		"""
		Returns the density at 295K in g/cm3 respectively g/L.

		:rtype: float
		"""

		return self._density

	@memoized_property
	def eleconfig(self) -> str:
		"""
		Returns the Ground state electron configuration.

		:rtype: str
		"""

		return self._eleconfig

	@memoized_property
	def oxistates(self) -> str:
		"""
		Returns the oxidation states

		:rtype: str
		"""

		return self._oxistates

	@memoized_property
	def ionenergy(self) -> Tuple:  # TODO
		"""
		Returns the ionization energies in eV
		"""

		return self._ionenergy

	@memoized_property
	def isotopes(self) -> Dict[int, "Isotope"]:
		"""
		Returns the Isotopic composition.

		keys: isotope mass number

		values: Isotope(relative atomic mass, abundance)
		"""

		return self._isotopes

	@memoized_property
	def description(self):
		return self._description

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		ionenergy_list = []

		for i, j in enumerate(self.ionenergy):
			if i and (i % 5 == 0):
				ionenergy_list.append(f'\n        {j}')
			else:
				ionenergy_list.append(f'{j}')

		ionenergy = ', '.join(ionenergy_list)

		if len(self.ionenergy) > 5:
			ionenergy = f'(\n        {ionenergy},\n    )'
		elif len(self.ionenergy) == 1:
			ionenergy = f'({ionenergy},)'
		else:
			ionenergy = f'({ionenergy})'

		isotopes_list = []

		for massnum in sorted(self.isotopes):
			iso = self.isotopes[massnum]
			isotopes_list.append(f'{massnum}: Isotope({iso.mass}, {iso.abundance}, {massnum})')

		isotopes = ',\n        '.join(isotopes_list)

		if len(self.isotopes) > 1:
			isotopes = f'{{\n        {isotopes},\n    }},'
		else:
			isotopes = f'{{{isotopes}}},'

		return ',\n    '.join((
				f"Element(\n    {self.number}, '{self.symbol}', '{self.name}'",
				f"group={self.group}, period={self.period},"
				f" block='{self.block}', series={self.series}",
				f"mass={self.mass}, eleneg={self.eleneg},"
				f" eleaffin={self.eleaffin}",
				f"covrad={self.covrad}, atmrad={self.atmrad},"
				f" vdwrad={self.vdwrad}",
				f"tboil={self.tboil}, tmelt={self.tmelt}, density={self.density}",
				f"eleconfig='{self.eleconfig}'",
				f"oxistates='{self.oxistates}'",
				f"ionenergy={ionenergy}",
				f"isotopes={isotopes}\n)"
				))

	@memoized_property
	def nominalmass(self) -> int:
		"""
		Return mass number of most abundant natural stable isotope.
		"""

		nominalmass = 0
		maxabundance = 0

		for massnum, iso in self.isotopes.items():
			if iso.abundance > maxabundance:
				maxabundance = iso.abundance
				nominalmass = massnum

		return nominalmass

	@memoized_property
	def neutrons(self) -> int:
		"""
		Returns the number of neutrons in the most abundant natural stable isotope.
		"""

		return self.nominalmass - self.protons

	@memoized_property
	def exactmass(self) -> float:
		"""
		Returns the relative atomic mass calculated from the isotopic composition.
		"""

		return sum(iso.mass * iso.abundance for iso in self.isotopes.values())

	@memoized_property
	def eleconfig_dict(self) -> Dict[Tuple, int]:  # TODO
		"""
		Returns the ground state electron configuration.

		Mapping of Tuple(shell, subshell): electrons.
		"""

		adict = {}
		if self.eleconfig.startswith('['):
			base = self.eleconfig.split(' ', 1)[0][1:-1]
			adict.update(_elements.ELEMENTS[base].eleconfig_dict)
		for e in self.eleconfig.split()[bool(adict):]:
			adict[(int(e[0]), e[1])] = int(e[2:]) if len(e) > 2 else 1
		return adict

	@memoized_property
	def eleshells(self) -> Tuple[int, ...]:
		"""
		Return number of electrons per shell as tuple.
		"""

		eleshells = [0, 0, 0, 0, 0, 0, 0]
		for key, val in self.eleconfig_dict.items():
			eleshells[key[0] - 1] += val
		return tuple(ele for ele in eleshells if ele)

	def validate(self) -> None:
		"""
		Check consistency of data. Raise Error on failure.
		"""

		assert self.period in _table.PERIODS
		assert self.group in _table.GROUPS
		assert self.block in _table.BLOCKS
		assert self.series in _table.SERIES

		if self.number != self.protons:
			raise ValueError(f'{self.symbol} - atomic number must equal proton number')

		if self.protons != sum(self.eleshells):
			raise ValueError(f'{self.symbol} - number of protons must equal electrons')

		if len(self.ionenergy) > 1:
			ionev_ = self.ionenergy[0]
			for ionev in self.ionenergy[1:]:
				if ionev <= ionev_:
					raise ValueError(f'{self.symbol} - ionenergy not increasing')
				ionev_ = ionev

		mass = 0.0
		frac = 0.0

		for iso in self.isotopes.values():
			mass += iso.abundance * iso.mass
			frac += iso.abundance

		if abs(mass - self.mass) > 0.03:
			raise ValueError(
					f'{self.symbol} - average of isotope masses '
					f'({mass:.4f}) != mass ({self.mass:.4f})'
					)

		if abs(frac - 1.0) > 1e-9:
			raise ValueError(f'{self.symbol} - sum of isotope abundances != 1.0')


class Isotope(Dictable):
	"""
	Isotope massnumber, relative atomic mass, and abundance.
	"""

	def __init__(self, mass: float = 0.0, abundance: float = 1.0, massnumber: int = 0):
		super().__init__()

		self._mass: float = mass
		self._abundance: float = abundance
		self._massnumber: int = massnumber

	@memoized_property
	def mass(self) -> float:
		return self._mass

	@memoized_property
	def abundance(self) -> float:
		return self._abundance

	@memoized_property
	def massnumber(self) -> int:
		return self._massnumber

	def __str__(self) -> str:
		return f'{self.massnumber}, {self.mass:.4f}, {self.abundance * 100:.6f}%'

	def __repr__(self) -> str:
		return f'Isotope({repr(self.mass)}, {repr(self.abundance)}, {repr(self.massnumber)})'

	@property
	def __dict__(self):
		return dict(
				mass=self.mass,
				abundance=self.abundance,
				massnumber=self.massnumber,
				)


# Isotope 0 Key:
# mass of the most abundant isotope and 1.0 abundance.


# TODO: make frozen
class Elements:
	"""
	Ordered dict of Elements with lookup by number, symbol, and name.
	"""

	def __init__(self, *elements):
		self._list = []
		self._dict = {}

		for element in elements:
			if element.number > len(self._list) + 1:
				raise ValueError('Elements must be added in order')
			if element.number <= len(self._list):
				self._list[element.number - 1] = element
			else:
				self._list.append(element)

			self._dict[element.number] = element
			self._dict[element.symbol] = element
			self.add_alternate_spelling(element, element.name)

	def __str__(self) -> str:
		return f'[{", ".join(ele.symbol for ele in self._list)}]'

	def __repr__(self) -> str:
		elements = ',\n    '.join(
				'\n    '.join(line for line in repr(element).splitlines()) for element in self._list
				)
		elements = f'Elements(\n    {elements},\n)'
		return elements

	def __contains__(self, item) -> bool:
		return item in self._dict

	def __iter__(self):
		return iter(self._list)

	def __len__(self) -> int:
		return len(self._list)

	def __getitem__(self, key):
		if isinstance(key, str):
			try:
				return self._dict[key.casefold()]
			except KeyError:
				return self._dict[key]
		elif isinstance(key, int):
			return self._dict[key]
		elif isinstance(key, float):
			return self._dict[int(key)]
		elif isinstance(key, slice):
			start, stop, step = key.indices(len(self._list))
			return self._list[slice(start - 1, stop - 1, step)]
		else:
			try:
				symbol, isotope = self.split_isotope(key)
				return self._dict[symbol.capitalize()]
			except:
				raise KeyError(f"Unknown key: '{key}'")

	@lru_cache()
	def split_isotope(self, string: str):
		from chemistry_tools.formulae.formula import _split_isotope
		return _split_isotope(string)

	def add_alternate_spelling(self, element: Element, spelling: str):
		self._dict[spelling] = element
		self._dict[spelling.lower()] = element
		self._dict[spelling.casefold()] = element

	@memoized_property
	def symbols(self) -> List[str]:
		return [element.symbol for element in sorted(self._list, key=lambda e: e.number)]

	@memoized_property
	def names(self) -> List[str]:
		return [str(element) for element in sorted(self._list, key=lambda e: e.number)]

	@memoized_property
	def lower_names(self) -> List[str]:
		return [str(element).lower() for element in sorted(self._list, key=lambda e: e.number)]


@doctools.append_docstring_from(Element)
class HeavyHydrogen(Element):
	"""
	Subclass of Element to handle the Heavy Hydrogen isotopes Deuterium and Tritium
	"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.symbol not in {"D", "T"}:
			raise ValueError("'HeavyHydrogen' can only be used for Deuterium and Tritium")

	@memoized_property
	def nominalmass(self) -> int:
		"""
		Return mass number of most abundant natural stable isotope.

		:rtype: int
		"""

		if self.symbol == "D":
			return 2
		elif self.symbol == "T":
			return 3
		else:
			raise ValueError("Unknown heavy hydrogen isotope.")

	@memoized_property
	def as_isotope(self) -> str:
		"""
		Return the isotope in H[X] format

		:rtype: str
		"""

		return f'H[{self.nominalmass}]'
