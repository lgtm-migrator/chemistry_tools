#!/usr/bin/env python3
#
#  units.py
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
#  Based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from collections import OrderedDict

# 3rd party
import numpy  # type: ignore
import quantities  # type: ignore
import quantities.markup  # type: ignore

__all__ = ["latex_of_unit", "compare_equality", "allclose", "format_string"]


def latex_of_unit(quant):
	r"""
	Returns LaTeX reperesentation of the unit of a quantity

	**Examples**
	>>> print(latex_of_unit(1/quantities.kelvin))
	\mathrm{\frac{1}{K}}
	"""

	# see https://github.com/python-quantities/python-quantities/issues/148
	return quantities.markup.format_units_latex(quant.dimensionality, mult=r"\\cdot").strip('$')


# NumPy like functions for compatibility:


def compare_equality(a, b) -> bool:
	"""
	Returns ``True`` if two arguments are equal.
	Both arguments need to have the same dimensionality.

	**Examples**
	>>> km, m = quantities.kilometre, quantities.metre
	>>> compare_equality(3*km, 3)
	False
	>>> compare_equality(3*km, 3000*m)
	True

	:param a:
	:type a: quantity
	:param b:
	:type b: quantity
	"""

	# Work around for https://github.com/python-quantities/python-quantities/issues/146
	try:
		a + b
	except TypeError:
		# We might be dealing with e.g. None (None + None raises TypeError)
		try:
			len(a)
		except TypeError:
			# Assumed scalar
			return a == b
		else:
			if len(a) != len(b):
				return False
			return all(compare_equality(_a, _b) for _a, _b in zip(a, b))
	except ValueError:
		return False
	else:
		return a == b


def allclose(a, b, rtol=1e-8, atol=None):
	"""
	Analogous to ``numpy.allclose``.
	"""

	try:
		d = abs(a - b)
	except Exception:
		try:
			if len(a) == len(b):
				return all(allclose(_a, _b, rtol, atol) for _a, _b in zip(a, b))
			else:
				return False
		except Exception:
			return False
	lim = abs(a) * rtol
	if atol is not None:
		lim += atol

	try:
		len(d)
	except TypeError:
		return d <= lim
	else:
		try:
			len(lim)
		except TypeError:
			return numpy.all([_d <= lim for _d in d])
		else:
			return numpy.all([_d <= _lim for _d, _lim in zip(d, lim)])


# TODO: decide whether to deprecate in favor of "number_to_scientific_latex"?
def format_string(value, precision="%.5g", tex=False):
	"""
	Formats a scalar with unit as two strings

	:param value: Value with unit
	:type value: float
	:param precision:
	:type precision: str, optional
	:param tex: Whether the string should be formatted for LaTex. Default :const:`False`
	:type tex: bool, optional

	:return:
	:rtype:

	**Examples**
	>>> print(' '.join(format_string(0.42*quantities.mol/quantities.decimetre**3)))
	0.42 mol/decimetre**3
	>>> print(' '.join(format_string(2/quantities.s, tex=True)))
	2 \\mathrm{\\frac{1}{s}}
	"""

	if tex:
		unit_str = latex_of_unit(value)
	else:
		attr = "unicode" if quantities.markup.config.use_unicode else "string"
		unit_str = getattr(value.dimensionality, attr)
	return precision % float(value.magnitude), unit_str


# Additional units to complement quantities
per100eV = quantities.UnitQuantity(
		"per_100_eV", 1 / (100 * quantities.eV * quantities.constants.Avogadro_constant), u_symbol="(100eV)**-1"
		)
dm = decimetre = quantities.UnitQuantity("decimetre", quantities.m / 10.0, u_symbol="dm")
m3 = quantities.metre**3
dm3 = decimetre**3
cm3 = quantities.centimetre**3
nanomolar = quantities.UnitQuantity("nM", 1e-6 * quantities.mole / m3, u_symbol="nM")
molal = quantities.UnitQuantity("molal", quantities.mole / quantities.kg, u_symbol="molal")
micromole = quantities.UnitQuantity("micromole", quantities.mole / 1e6, u_symbol="μmol")
nanomole = quantities.UnitQuantity("nanomole", quantities.mole / 1e9, u_symbol="nmol")
kilojoule = quantities.UnitQuantity("kilojoule", 1e3 * quantities.joule, u_symbol="kJ")
kilogray = quantities.UnitQuantity("kilogray", 1e3 * quantities.gray, u_symbol="kGy")
perMolar_perSecond = 1 / quantities.molar / quantities.s
umol_per_J = quantities.umol / quantities.joule

# unit registry data and logic:
SI_base_registry = {
		"length": quantities.metre,
		"mass": quantities.kilogram,
		"time": quantities.second,
		"current": quantities.ampere,
		"temperature": quantities.kelvin,
		"luminous_intensity": quantities.candela,
		"amount": quantities.mole
		}

dimension_codes = {
		"length": 'L',
		"mass": 'M',
		"time": 'T',
		"current": 'I',
		"temperature": 'Θ',
		"amount": 'N',
		}
