#!/usr/bin/env python3
#
#  test_printing.py
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


import quantities  # type: ignore

from chempy.printing import (
	_float_str_w_uncert, number_to_scientific_html, number_to_scientific_latex,
	number_to_scientific_unicode,
	)


from collections import OrderedDict

from chempy import Substance
from chempy.printing import html
from chempy.printing import as_per_substance_html_table

def test__float_str_w_uncert():
	assert _float_str_w_uncert(-5739, 16.34, 2) == '-5739(16)'
	assert _float_str_w_uncert(-5739, 16.9, 2) == '-5739(17)'
	assert _float_str_w_uncert(0.0123, 0.00169, 2) == '0.0123(17)'
	assert _float_str_w_uncert(0.01234, 0.00169, 2) == '0.0123(17)'
	assert _float_str_w_uncert(0.01234, 0.0016501, 2) == '0.0123(17)'
	assert _float_str_w_uncert(0.01234, 0.0016501, 1) == '0.012(2)'
	assert _float_str_w_uncert(-9.99752e15, 349e10, 2) == '-9.9975(35)e15'
	assert _float_str_w_uncert(-9.99752e5, 349, 2) == '-999750(350)'
	assert _float_str_w_uncert(-9.99752e5, 349, 3) == '-999752(349)'
	assert _float_str_w_uncert(315, 17.9e-4, 2) == '315.0000(18)'


def test_number_to_scientific_html():
	assert number_to_scientific_html(2e-17) == '2&sdot;10<sup>-17</sup>'
	assert number_to_scientific_html(1e-17) == '10<sup>-17</sup>'


def test_number_to_scientific_latex():
	assert number_to_scientific_latex(2e-17) == r'2\cdot 10^{-17}'
	assert number_to_scientific_latex(1e-17) == '10^{-17}'
	assert number_to_scientific_latex(315, 17.9e-4, fmt=2) == '315.0000(18)'


def test_number_to_scientific_latex__units():
	from chemistry_tools import units
	
	assert number_to_scientific_latex(315*quantities.km, 17.9*units.dm, fmt=2) == r'315.0000(18)\,\mathrm{km}'
	assert number_to_scientific_latex(315*quantities.km, 17.9*units.dm, quantities.m, fmt=2) == r'315000.0(18)\,\mathrm{m}'
	assert number_to_scientific_latex(1319*quantities.km, 41207*quantities.m, quantities.m, fmt=1) == r'1.32(4)\cdot 10^{6}\,\mathrm{m}'


def test_number_to_scientific_unicode():
	assert number_to_scientific_unicode(2e-17) == u'2·10⁻¹⁷'
	assert number_to_scientific_unicode(1e-17) == u'10⁻¹⁷'



def test_as_per_substance_html_table():
	substances = OrderedDict([(k, Substance.from_formula(k)) for k in 'H OH'.split()])
	assert html(as_per_substance_html_table([2, 3], substances)).count('<tr>') == 3
	assert html(as_per_substance_html_table({'H': 2, 'OH': 3}, substances)).count('<tr>') == 3
