#!/usr/bin/env python3
#
#  test_py
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
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

# 3rd party
import numpy
import quantities  # type: ignore

# this package
from chemistry_tools import units

UncertainQuantity = quantities.UncertainQuantity


def test_default_units():
	assert quantities.ampere
	assert quantities.candela
	assert quantities.centimetre
	assert quantities.eV
	assert quantities.gram
	assert quantities.gray
	assert quantities.hour
	assert quantities.joule
	assert quantities.kelvin
	assert quantities.kilogram
	assert quantities.metre
	assert quantities.MeV
	assert quantities.micrometre
	assert quantities.molar
	assert quantities.mole
	assert quantities.nanometre
	assert quantities.second
	assert quantities.umol
	assert units.umol_per_J
	assert units.decimetre
	assert units.per100eV
	assert units.perMolar_perSecond


def test_allclose():
	# this package
	from chemistry_tools.units import allclose

	assert allclose(42, 42)
	assert allclose(42 * quantities.meter, 0.042 * quantities.km)
	assert not allclose(42, 43)
	assert not allclose(42, 42 * quantities.meter)
	assert not allclose(42, 43 * quantities.meter)
	assert not allclose(42 * quantities.meter, 42)

	a = numpy.linspace(2, 3) * quantities.second
	b = numpy.linspace(2 / 3600., 3 / 3600.) * quantities.hour
	assert allclose(a, b)
	assert allclose(
			[3600 * quantities.second, 2 * quantities.metre / quantities.hour],
			[1 * quantities.hour, 2 / 3600 * quantities.metre / quantities.second],
			)
	c1 = [[3000, 4000], [3000, 4000]] * quantities.mol / units.m3
	c2 = [[3000, 4000], [436.2, 5281.89]] * quantities.mol / units.m3
	assert not allclose(c1, c2)
	assert allclose(0 * quantities.second, 0 * quantities.second)

	# Possibly allow comparison with scalars in future (broadcasting):
	# assert allclose(2, [2, 2])
	# assert allclose([2, 2], 2)
	#
	# assert not allclose(2, [2, 3])
	# assert not allclose([2, 3], 2)
	#
	# assert allclose(2*quantities.second, [2, 2]*quantities.second)
	# assert allclose([2, 2]*quantities.second, 2*quantities.second)
	#
	# assert not allclose(2*quantities.second, [2, 3]*quantities.second)
	# assert not allclose([2, 3]*quantities.second, 2*quantities.second)


def test_UncertainQuantity():
	a = UncertainQuantity([1, 2], quantities.m, [.1, .2])
	assert a[1] == [2.] * quantities.m
	assert (-a)[0] == [-1.] * quantities.m
	assert (-a).uncertainty[0] == [0.1] * quantities.m
	assert (-a)[0] == (a * -1)[0]
	assert (-a).uncertainty[0] == (a * -1).uncertainty[0]


def test_compare_equality():
	assert units.compare_equality(3 * quantities.m, 3 * quantities.m)
	assert units.compare_equality(3 * quantities.m, 3e-3 * quantities.km)
	assert units.compare_equality(3e+3 * quantities.mm, 3 * quantities.m)
	assert not units.compare_equality(3 * quantities.m, 2 * quantities.m)
	assert not units.compare_equality(3 * quantities.m, 3 * quantities.s)
	assert not units.compare_equality(3 * quantities.m, 3 * quantities.m**2)
	assert not units.compare_equality(3 * quantities.m, numpy.array(3))
	assert not units.compare_equality(numpy.array(3), 3 * quantities.m)
	assert units.compare_equality([3, None], [3, None])
	assert not units.compare_equality([3, None, 3], [3, None, None])
	assert not units.compare_equality([None, None, 3], [None, None, 2])
	assert units.compare_equality([3 * quantities.m, None], [3, None])
	assert not units.compare_equality([3 * quantities.m, None], [3 * quantities.km, None])


def test_format_string():
	assert units.format_string(3 * quantities.gram / quantities.metre**2) == ('3', "g/m**2")
	assert units.format_string(
			3 * quantities.gram / quantities.metre**2, tex=True
			) == ('3', r"\mathrm{\frac{g}{m^{2}}}")


def test_joule_html():
	joule_htm = "kg&sdot;m<sup>2</sup>/s<sup>2</sup>"
	joule = quantities.J.dimensionality.simplified
	assert joule.html == joule_htm


def test_as_latex():
	assert units.as_latex(quantities.gram / quantities.metre**2) == r"\mathrm{\frac{g}{m^{2}}}"
