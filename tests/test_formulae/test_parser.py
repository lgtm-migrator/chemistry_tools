#!/usr/bin/env python3
#
#  test_parser.py
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
import decimal

# 3rd party
import pytest  # type: ignore

# this package
from chemistry_tools.formulae.html import string_to_html
from chemistry_tools.formulae.latex import string_to_latex
from chemistry_tools.formulae.parser import mass_from_composition, relative_atomic_masses, string_to_composition
from chemistry_tools.formulae.unicode import string_to_unicode

# this package
from mathematical.utils import rounders  # type: ignore # TODO


def test_formula_to_composition():
	assert string_to_composition('H2O') == {"H": 2, "O": 1}
	assert string_to_composition('Fe+3') == {0: 3, "Fe": 1}
	assert string_to_composition('Na+1') == {0: 1, "Na": 1}
	assert string_to_composition('Na+') == {0: 1, "Na": 1}
	assert string_to_composition('Cl-') == {0: -1, "Cl": 1}
	assert string_to_composition('NaCl') == {"Na": 1, "Cl": 1}
	assert string_to_composition('NaCl(s)') == {"Na": 1, "Cl": 1}
	assert string_to_composition('Fe(SCN)2+') == {0: 1, "C": 2, "N": 2, "S": 2, "Fe": 1}
	assert string_to_composition('Fe(SCN)2+1') == {0: 1, "C": 2, "N": 2, "S": 2, "Fe": 1}
	assert string_to_composition('((H2O)2OH)12') == {"H": 60, "O": 36}

	# Special case: solvated electron:
	assert string_to_composition('e-') == {0: -1}
	assert string_to_composition('e-1') == {0: -1}
	assert string_to_composition('e-(aq)') == {0: -1}
	assert string_to_composition('SO4-2(aq)') == {0: -2, "O": 4, "S": 1}

	# prefixes and suffixes
	assert string_to_composition('.NO2(g)') == {"N": 1, "O": 2}
	assert string_to_composition('.NH2') == {"H": 2, "N": 1}
	assert string_to_composition('ONOOH') == {"H": 1, "N": 1, "O": 3}
	assert string_to_composition('.ONOO') == {"N": 1, "O": 3}
	assert string_to_composition('.NO3-2') == {0: -2, "N": 1, "O": 3}

	with pytest.raises(ValueError):
		string_to_composition('F-F')

	# TODO: parse greek prefixes
	# assert string_to_composition('alpha-FeOOH(s)') == {"H": 1, "O": 2, "Fe": 1}
	# assert string_to_composition('epsilon-Zn(OH)2(s)') == {"H": 2, "O": 2, "Zn": 1}

	assert string_to_composition('Na2CO3.7H2O(s)') == {"Na": 2, "C": 1, "O": 10, "H": 14}


@pytest.mark.parametrize(
		"string, expected",
		[
				('H2O', 'H_{2}O'),
				('C6H6+', 'C_{6}H_{6}^{+}'),
				('Fe(CN)6-3', 'Fe(CN)_{6}^{3-}'),
				('C18H38+2', 'C_{18}H_{38}^{2+}'),
				('((H2O)2OH)12', '((H_{2}O)_{2}OH)_{12}'),
				('NaCl', 'NaCl'),
				('NaCl(s)', 'NaCl(s)'),
				('e-(aq)', 'e^{-}(aq)'),
				('Ca+2(aq)', 'Ca^{2+}(aq)'),
				('.NO2(g)', r'^\bullet NO_{2}(g)'),
				('.NH2', r'^\bullet NH_{2}'),
				('ONOOH', 'ONOOH'),
				('.ONOO', r'^\bullet ONOO'),
				('.NO3-2', r'^\bullet NO_{3}^{2-}'),
				('alpha-FeOOH(s)', r'\alpha-FeOOH(s)'),
				('epsilon-Zn(OH)2(s)', r'\varepsilon-Zn(OH)_{2}(s)'),
				('Na2CO3.7H2O(s)', r'Na_{2}CO_{3}\cdot 7H_{2}O(s)'),
				('Na2CO3.1H2O(s)', r'Na_{2}CO_{3}\cdot H_{2}O(s)'),
				]
		)
def test_formula_to_latex(string, expected):
	assert string_to_latex(string) == expected


@pytest.mark.parametrize(
		"string, expected",
		[
				('NH4+', 'NH₄⁺'),
				('H2O', 'H₂O'),
				('C6H6+', 'C₆H₆⁺'),
				('Fe(CN)6-3', 'Fe(CN)₆³⁻'),
				('C18H38+2', 'C₁₈H₃₈²⁺'),
				('((H2O)2OH)12', '((H₂O)₂OH)₁₂'),
				('NaCl', 'NaCl'),
				('NaCl(s)', 'NaCl(s)'),
				('e-(aq)', 'e⁻(aq)'),
				('Ca+2(aq)', 'Ca²⁺(aq)'),
				('.NO2(g)', '⋅NO₂(g)'),
				('.NH2', '⋅NH₂'),
				('ONOOH', 'ONOOH'),
				('.ONOO', '⋅ONOO'),
				('.NO3-2', '⋅NO₃²⁻'),
				('alpha-FeOOH(s)', 'α-FeOOH(s)'),
				('epsilon-Zn(OH)2(s)', 'ε-Zn(OH)₂(s)'),
				('Na2CO3.7H2O(s)', 'Na₂CO₃·7H₂O(s)'),
				('Na2CO3.1H2O(s)', 'Na₂CO₃·H₂O(s)'),
				]
		)
def test_formula_to_unicode(string, expected):
	assert string_to_unicode(string) == expected


@pytest.mark.parametrize(
		"string, expected",
		[
				('H2O', 'H<sub>2</sub>O'),
				('C6H6+', 'C<sub>6</sub>H<sub>6</sub><sup>+</sup>'),
				('Fe(CN)6-3', 'Fe(CN)<sub>6</sub><sup>3-</sup>'),
				('C18H38+2', 'C<sub>18</sub>H<sub>38</sub><sup>2+</sup>'),
				('((H2O)2OH)12', '((H<sub>2</sub>O)<sub>2</sub>OH)<sub>12</sub>'),
				('NaCl', 'NaCl'),
				('NaCl(s)', 'NaCl(s)'),
				('e-(aq)', 'e<sup>-</sup>(aq)'),
				('Ca+2(aq)', 'Ca<sup>2+</sup>(aq)'),
				('.NO2(g)', r'&sdot;NO<sub>2</sub>(g)'),
				('.NH2', r'&sdot;NH<sub>2</sub>'),
				('ONOOH', 'ONOOH'),
				('.ONOO', r'&sdot;ONOO'),
				('.NO3-2', r'&sdot;NO<sub>3</sub><sup>2-</sup>'),
				('alpha-FeOOH(s)', r'&alpha;-FeOOH(s)'),
				('epsilon-Zn(OH)2(s)', (r'&epsilon;-Zn(OH)<sub>2</sub>(s)')),
				('Na2CO3.7H2O(s)', 'Na<sub>2</sub>CO<sub>3</sub>&sdot;7H<sub>2</sub>O(s)'),
				('Na2CO3.1H2O(s)', 'Na<sub>2</sub>CO<sub>3</sub>&sdot;H<sub>2</sub>O(s)'),
				]
		)
def test_formula_to_html(string, expected):
	assert string_to_html(string) == expected


def test_mass_from_composition():
	mass1 = mass_from_composition({11: 1, 9: 1})
	assert rounders(mass1, "0.000000") == decimal.Decimal("41.988172")

	mass2 = mass_from_composition({"Na": 1, "F": 1})
	assert mass1 == mass2
	assert rounders(mass2, "0.000000") == decimal.Decimal("41.988172")


def test_relative_atomic_masses():
	assert rounders(relative_atomic_masses[0], "0.0000") == decimal.Decimal("1.0079")


def test_mass_from_composition__formula():
	mass = mass_from_composition(string_to_composition('NaF'))
	assert rounders(mass, "0.000000") == decimal.Decimal("41.988172")

	Fminus = mass_from_composition(string_to_composition('F/-'))
	assert abs(Fminus - 18.998403163 - 5.489e-4) < 1e-7
