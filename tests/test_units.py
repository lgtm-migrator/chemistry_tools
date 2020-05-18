#!/usr/bin/env python3
#
#  test_units.py
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


from collections import defaultdict

import numpy as np
import pytest

from chemistry_tools.units import (
	_sum, allclose, Backend, compare_equality, concatenate, default_unit_in_registry,
	fold_constants, format_string, get_derived_unit, get_physical_dimensionality, is_unitless,
	latex_of_unit, logspace_from_lin, SI_base_registry,
	to_unitless, uniform, unit_of, unit_registry_from_human_readable,
	unit_registry_to_human_readable, unitless_in_registry
	)

from chemistry_tools import units

import quantities
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
	assert allclose(42, 42)
	assert allclose(42 * quantities.meter, 0.042 * quantities.km)
	assert not allclose(42, 43)
	assert not allclose(42, 42 * quantities.meter)
	assert not allclose(42, 43 * quantities.meter)
	assert not allclose(42 * quantities.meter, 42)

	a = np.linspace(2, 3) * quantities.second
	b = np.linspace(2 / 3600., 3 / 3600.) * quantities.hour
	assert allclose(a, b)
	assert allclose(
			[3600 * quantities.second, 2 * quantities.metre / quantities.hour],
			[1 * quantities.hour, 2 / 3600 * quantities.metre / quantities.second])
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


def test_is_unitless():
	assert not is_unitless(1 * quantities.second)
	assert is_unitless(1)
	assert is_unitless({'a': 1, 'b': 2.0})
	assert not is_unitless({'a': 2, 'b': 5.0 * quantities.second, 'c': 3})
	assert is_unitless(7 * quantities.molar / quantities.mole * units.dm3)
	assert is_unitless([2, 3, 4])
	assert not is_unitless([2 * quantities.m, 3 * quantities.m])
	assert not is_unitless([3, 4 * quantities.m])
	assert is_unitless(quantities.dimensionless)  # this was causing RecursionError


def test_unit_of():
	assert compare_equality(unit_of(0.1 * quantities.metre / quantities.second), quantities.metre / quantities.second)
	assert not compare_equality(unit_of(0.1 * quantities.metre / quantities.second), quantities.kilometre / quantities.second)
	assert compare_equality(unit_of(7), 1)
	assert unit_of(quantities.gray).dimensionality == quantities.gray.dimensionality
	ref = (quantities.joule / quantities.kg).simplified.dimensionality
	assert unit_of(quantities.gray, simplified=True).dimensionality == ref

	assert compare_equality(unit_of(dict(foo=3 * quantities.molar, bar=2 * quantities.molar)), quantities.molar)
	assert not compare_equality(unit_of(dict(foo=3 * quantities.molar, bar=2 * quantities.molar)), quantities.second)
	with pytest.raises(Exception):
		unit_of(dict(foo=3 * quantities.molar, bar=2 * quantities.second))
	assert not compare_equality(unit_of(dict(foo=3 * quantities.molar, bar=2 * quantities.molar)), quantities.mol / quantities.metre**3)


def test_to_unitless():
	dm = units.decimetre
	vals = [1.0 * dm, 2.0 * dm]
	result = to_unitless(vals, quantities.metre)
	assert result[0] == 0.1
	assert result[1] == 0.2
	with pytest.raises(ValueError):
		to_unitless([42, 43], quantities.metre)

	with pytest.raises(ValueError):
		to_unitless(np.array([42, 43]), quantities.metre)

	vals = [1.0, 2.0] * dm
	result = to_unitless(vals, quantities.metre)
	assert result[0] == 0.1
	assert result[1] == 0.2

	length_unit = 1000 * quantities.metre
	result = to_unitless(1.0 * quantities.metre, length_unit)
	assert abs(result - 1e-3) < 1e-12

	amount_unit = 1e-9  # nano
	assert abs(to_unitless(1.0, amount_unit) - 1e9) < 1e-6
	assert abs(to_unitless(
			3 / (quantities.second * quantities.molar),
			quantities.metre**3 / quantities.mole / quantities.second) - 3e-3
			) < 1e-12
	assert abs(to_unitless(2 * units.dm3, units.cm3) - 2000) < 1e-12
	assert abs(to_unitless(2 * units.m3, units.dm3) - 2000) < 1e-12
	assert (float(to_unitless(UncertainQuantity(2, units.dm3, .3), units.cm3)) - 2000) < 1e-12

	g1 = UncertainQuantity(4.46, units.per100eV, 0)
	g_unit = get_derived_unit(SI_base_registry, 'radiolytic_yield')
	assert abs(to_unitless(g1, g_unit) - 4.46 * 1.036e-7) < 1e-9
	g2 = UncertainQuantity(-4.46, units.per100eV, 0)
	assert abs(to_unitless(-g2, g_unit) - 4.46 * 1.036e-7) < 1e-9

	vals = np.array([1. * dm, 2. * dm], dtype=object)
	result = to_unitless(vals, quantities.metre)
	assert result[0] == 0.1
	assert result[1] == 0.2

	one_billionth_molar_in_nanomolar = to_unitless(1e-9 * quantities.molar, units.nanomolar)
	assert one_billionth_molar_in_nanomolar == 1


def test_UncertainQuantity():
	a = UncertainQuantity([1, 2], quantities.m, [.1, .2])
	assert a[1] == [2.] * quantities.m
	assert (-a)[0] == [-1.] * quantities.m
	assert (-a).uncertainty[0] == [0.1] * quantities.m
	assert (-a)[0] == (a * -1)[0]
	assert (-a).uncertainty[0] == (a * -1).uncertainty[0]


def test_linspace():
	ls = np.linspace(2 * quantities.second, 3 * quantities.second)
	assert abs(to_unitless(ls[0], quantities.hour) - 2 / 3600.) < 1e-15


def test_logspace_from_lin():
	ls = logspace_from_lin(2 * quantities.second, 3 * quantities.second)
	assert abs(to_unitless(ls[0], quantities.hour) - 2 / 3600.) < 1e-15
	assert abs(to_unitless(ls[-1], quantities.hour) - 3 / 3600.) < 1e-15


def test_get_derived_unit():
	registry = SI_base_registry.copy()
	registry['length'] = 1e-1 * registry['length']
	conc_unit = get_derived_unit(registry, 'concentration')
	dm = units.decimetre
	assert abs(conc_unit - 1 * quantities.mole / (dm ** 3)) < 1e-12 * quantities.mole / (dm ** 3)

	registry = defaultdict(lambda: 1)
	registry['amount'] = 1e-9  # nano
	assert abs(to_unitless(1.0, get_derived_unit(
			registry, 'concentration')) - 1e9) < 1e-6


def test_unit_registry_to_human_readable():
	# Not as much human readable as JSON serializable...
	d = defaultdict(lambda: 1)
	assert unit_registry_to_human_readable(d) == {
			x: (1, 1) for x in SI_base_registry.keys()}

	ur = {
			'length': 1e3 * quantities.metre,
			'mass': 1e-2 * quantities.kilogram,
			'time': 1e4 * quantities.second,
			'current': 1e-1 * quantities.ampere,
			'temperature': 1e1 * quantities.kelvin,
			'luminous_intensity': 1e-3 * quantities.candela,
			'amount': 1e4 * quantities.mole
			}
	assert unit_registry_to_human_readable(ur) == {
			'length': (1e3, 'm'),
			'mass': (1e-2, 'kg'),
			'time': (1e4, 's'),
			'current': (1e-1, 'A'),
			'temperature': (1e1, 'K'),
			'luminous_intensity': (1e-3, 'cd'),
			'amount': (1e4, 'mol')
			}
	assert unit_registry_to_human_readable(ur) != {
			'length': (1e2, 'm'),
			'mass': (1e-2, 'kg'),
			'time': (1e4, 's'),
			'current': (1e-1, 'A'),
			'temperature': (1e1, 'K'),
			'luminous_intensity': (1e-3, 'cd'),
			'amount': (1e4, 'mol')
			}


def test_unit_registry_from_human_readable():
	hr = unit_registry_to_human_readable(defaultdict(lambda: 1))
	assert hr == {x: (1, 1) for x in SI_base_registry.keys()}
	ur = unit_registry_from_human_readable(hr)
	assert ur == {x: 1 for x in SI_base_registry.keys()}

	hr = unit_registry_to_human_readable(SI_base_registry)
	assert hr == {
			'length': (1.0, 'm'),
			'mass': (1.0, 'kg'),
			'time': (1.0, 's'),
			'current': (1.0, 'A'),
			'temperature': (1.0, 'K'),
			'luminous_intensity': (1.0, 'cd'),
			'amount': (1.0, 'mol')
			}
	ur = unit_registry_from_human_readable(hr)
	assert ur == SI_base_registry

	ur = unit_registry_from_human_readable({
			'length': (1.0, 'm'),
			'mass': (1.0, 'kg'),
			'time': (1.0, 's'),
			'current': (1.0, 'A'),
			'temperature': (1.0, 'K'),
			'luminous_intensity': (1.0, 'cd'),
			'amount': (1.0, 'mol')
			})
	assert ur == {
			'length': quantities.metre,
			'mass': quantities.kilogram,
			'time': quantities.second,
			'current': quantities.ampere,
			'temperature': quantities.kelvin,
			'luminous_intensity': quantities.candela,
			'amount': quantities.mole
			}

	ur = unit_registry_from_human_readable({
			'length': (1e3, 'm'),
			'mass': (1e-2, 'kg'),
			'time': (1e4, 's'),
			'current': (1e-1, 'A'),
			'temperature': (1e1, 'K'),
			'luminous_intensity': (1e-3, 'cd'),
			'amount': (1e4, 'mol')
			})
	assert ur == {
			'length': 1e3 * quantities.metre,
			'mass': 1e-2 * quantities.kilogram,
			'time': 1e4 * quantities.second,
			'current': 1e-1 * quantities.ampere,
			'temperature': 1e1 * quantities.kelvin,
			'luminous_intensity': 1e-3 * quantities.candela,
			'amount': 1e4 * quantities.mole
			}

	assert ur != {
			'length': 1e2 * quantities.metre,
			'mass': 1e-3 * quantities.kilogram,
			'time': 1e2 * quantities.second,
			'current': 1e-2 * quantities.ampere,
			'temperature': 1e0 * quantities.kelvin,
			'luminous_intensity': 1e-2 * quantities.candela,
			'amount': 1e3 * quantities.mole
			}


def test_unitless_in_registry():
	mag = unitless_in_registry(3 * units.per100eV, SI_base_registry)
	ref = 3 * 1.0364268834527753e-07
	assert abs(mag - ref) < 1e-14
	ul = unitless_in_registry([3 * units.per100eV, 5 * quantities.mol / quantities.J], SI_base_registry)
	assert np.allclose(ul, [ref, 5], rtol=1e-6)


def test_compare_equality():
	assert compare_equality(3 * quantities.m, 3 * quantities.m)
	assert compare_equality(3 * quantities.m, 3e-3 * quantities.km)
	assert compare_equality(3e+3 * quantities.mm, 3 * quantities.m)
	assert not compare_equality(3 * quantities.m, 2 * quantities.m)
	assert not compare_equality(3 * quantities.m, 3 * quantities.s)
	assert not compare_equality(3 * quantities.m, 3 * quantities.m ** 2)
	assert not compare_equality(3 * quantities.m, np.array(3))
	assert not compare_equality(np.array(3), 3 * quantities.m)
	assert compare_equality([3, None], [3, None])
	assert not compare_equality([3, None, 3], [3, None, None])
	assert not compare_equality([None, None, 3], [None, None, 2])
	assert compare_equality([3 * quantities.m, None], [3, None])
	assert not compare_equality([3 * quantities.m, None], [3 * quantities.km, None])


def test_get_physical_dimensionality():
	assert get_physical_dimensionality(3 * quantities.mole) == {'amount': 1}
	assert get_physical_dimensionality([3 * quantities.mole]) == {'amount': 1}
	assert get_physical_dimensionality(42) == {}


def test_default_unit_in_registry():
	mol_per_m3 = default_unit_in_registry(3 * quantities.molar, SI_base_registry)
	assert mol_per_m3.magnitude == 1
	assert mol_per_m3 == quantities.mole / quantities.metre ** 3

	assert default_unit_in_registry(3, SI_base_registry) == 1
	assert default_unit_in_registry(3.0, SI_base_registry) == 1


def test__sum():
	# sum() does not work here...
	assert (_sum([0.1 * quantities.metre, 1 * units.decimetre]) - 2 * units.decimetre) / quantities.metre == 0


def test_Backend():
	b = Backend()
	with pytest.raises(ValueError):
		b.exp(-3 * quantities.metre)
	assert abs(b.exp(1234 * quantities.metre / quantities.kilometre) - b.exp(1.234)) < 1e-14


def test_Backend__numpy():
	b = Backend(np)
	assert b.sum([1000 * quantities.metre / quantities.kilometre, 1], axis=0) == 2.0

	with pytest.raises(AttributeError):
		b.Piecewise


def test_Backend__sympy():
	sympy = pytest.importorskip("sympy")
	b = Backend('sympy')
	assert b.sin(b.pi) == 0

	with pytest.raises(AttributeError):
		b.min


def test_format_string():
	assert format_string(3 * quantities.gram / quantities.metre ** 2) == ('3', 'g/m**2')
	assert format_string(3 * quantities.gram / quantities.metre ** 2, tex=True) == ('3', r'\mathrm{\frac{g}{m^{2}}}')


def test_joule_html():
	joule_htm = 'kg&sdot;m<sup>2</sup>/s<sup>2</sup>'
	joule = quantities.J.dimensionality.simplified
	assert joule.html == joule_htm


def test_latex_of_unit():
	assert latex_of_unit(quantities.gram / quantities.metre ** 2) == r'\mathrm{\frac{g}{m^{2}}}'


def test_concatenate():
	a = [1, 2] * quantities.metre
	b = [2, 3] * quantities.mm
	ref = [1, 2, 2e-3, 3e-3] * quantities.metre
	assert allclose(concatenate((a, b)), ref)


def test_pow0():
	a = [1, 2] * quantities.metre
	b = a**0
	assert np.allclose(b, [1, 1])

	c = a**2
	assert allclose(c, [1, 4] * quantities.m ** 2)


def test_uniform():
	base = [3 * quantities.km, 200 * quantities.m]
	refs = [np.array([3000, 200]), np.array([3, 0.2])]

	def _check(case, ref):
		assert np.any(np.all(uniform(case).magnitude == ref, axis=1))
	_check(base, refs)
	_check(tuple(base), refs)
	keys = 'foo bar'.split()
	assert (uniform(dict(zip(keys, base)))) in [dict(zip(keys, r)) for r in refs]


def test_fold_constants():
	assert abs(fold_constants(quantities.constants.pi) - np.pi) < 1e-15
