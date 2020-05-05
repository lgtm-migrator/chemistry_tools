#!/usr/bin/env python3
#
#  test_arithmeticdict.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
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


from chemistry_tools.dicts import defaultkeydict, ArithmeticDict


def test_ArithmeticDict():
	d1 = ArithmeticDict(float, [('a', 1.0), ('b', 2.0)])
	d2 = ArithmeticDict(float, [('c', 5.0), ('b', 3.0)])
	d3 = d1 + d2
	assert d3['a'] == 1.0
	assert d3['b'] == 5.0
	assert d3['c'] == 5.0
	d3 += {'c': 1.0}
	assert d3['a'] == 1.0
	assert d3['b'] == 5.0
	assert d3['c'] == 6.0
	d4 = {'a': 7.0} + d1
	assert d4['a'] == 8.0
	d5 = d1 + {'a': 9.0}
	assert d5['a'] == 10.0
	
	d6 = d1 - d2
	assert d6 == {'a': 1.0, 'b': -1.0, 'c': -5.0}
	d6 -= d3
	assert d6 == {'b': -6.0, 'c': -11.0}


def test_ArithmeticDict_add():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d2 = d1 + 3
	assert d2['a'] == 4
	assert d2['b'] == 5
	d2 = 3 + d1
	assert d2['a'] == 4
	assert d2['b'] == 5
	assert d2['c'] == 0
	d3 = d1 + d2
	assert d3['a'] == 5
	assert d3['b'] == 7
	assert d3['c'] == 0


def test_ArithmeticDict_iadd():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d1 += 3
	assert d1['a'] == 4
	assert d1['b'] == 5
	assert d1['c'] == 0


def test_ArithmeticDict_sub():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d2 = d1 - 7
	assert d2['a'] == -6
	assert d2['b'] == -5
	d2 = 3 - d1
	assert d2['a'] == 2
	assert d2['b'] == 1
	assert d2['c'] == 0
	d3 = d1 - d2
	assert d3['a'] == -1
	assert d3['b'] == 1


def test_ArithmeticDict_isub():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d1 -= 7
	assert d1['a'] == -6
	assert d1['b'] == -5
	assert d1['c'] == 0


def test_ArithmeticDict_mul():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d2 = d1 * 3
	assert d2['a'] == 3
	assert d2['b'] == 6
	d2 = 3 * d1
	assert d2['a'] == 3
	assert d2['b'] == 6
	assert d2['c'] == 0
	d3 = d1 * d2
	assert d3['a'] == 3
	assert d3['b'] == 12
	assert d3['c'] == 0


def test_ArithmeticDict_imul():
	d1 = ArithmeticDict(int, [('a', 1), ('b', 2)])
	d1 *= 3
	assert d1['a'] == 3
	assert d1['b'] == 6
	assert d1['c'] == 0


def test_ArithmeticDict_div():
	d1 = ArithmeticDict(int, [('a', 6), ('b', 9)])
	
	d2 = d1 / 3
	assert d2['a'] == 2
	assert d2['b'] == 3
	
	d2 = d1.copy() / 3
	assert d2['a'] == 2
	assert d2['b'] == 3
	
	d2 = 54 / d1
	assert d2['a'] == 9
	assert d2['b'] == 6
	assert d2['c'] == 0
	
	d1['c'] = 1
	d3 = (6 * d2) / d1
	assert d3['a'] == 9
	assert d3['b'] == 4
	assert d3['c'] == 0


def test_ArithmeticDict_floordiv():
	d1 = ArithmeticDict(int, [('a', 6), ('b', 9)])
	
	d2 = d1 // 2
	assert d2['a'] == 3
	assert d2['b'] == 4
	
	d2 = d1.copy() // 5
	assert d2['a'] == 1
	assert d2['b'] == 1
	
	d2 = 55 // d1
	assert d2['a'] == 9
	assert d2['b'] == 6
	assert d2['c'] == 0
	
	d1['c'] = 1
	d3 = (6 * d2 + 1) // d1
	assert d3['a'] == 9
	assert d3['b'] == 4
	assert d3['c'] == 1


def test_ArithmeticDict_idiv():
	d1 = ArithmeticDict(int, [('a', 6), ('b', 9)])
	d1 /= 3
	assert d1['a'] == 2
	assert d1['b'] == 3
	assert d1['c'] == 0


def test_ArithmeticDict_div_float():
	d = ArithmeticDict(float)
	d['a'] = 6.0
	d['b'] = 9.0
	t = d / 3.0
	assert t['a'] == 2.0
	assert t['b'] == 3.0


def test_ArithmeticDict_isclose():
	d1 = ArithmeticDict(float)
	d2 = ArithmeticDict(float)
	assert d1.isclose(d2)
	d1['a'] = 2
	assert not d1.isclose(d2)
	d2['a'] = 2 + 1e-15
	assert d1.isclose(d2)
	d2['b'] = 1e-15
	assert not d1.isclose(d2)
	assert d1.isclose(d2, atol=1e-14)


def test_ArithmeticDict_all_non_negative():
	d1 = ArithmeticDict(float)
	assert d1.all_non_negative()
	d1['a'] = .1
	assert d1.all_non_negative()
	d1['b'] = 0
	assert d1.all_non_negative()
	d1['b'] -= 1e-15
	assert not d1.all_non_negative()


def test_ArithmeticDict_eq():
	d1 = ArithmeticDict(int, a=1, b=0)
	d2 = ArithmeticDict(int, a=1, b=1)
	d3 = ArithmeticDict(int, a=1)
	assert not d1 == d2
	assert d1 == d3


def test_defaultkeydict():
	d = defaultkeydict(lambda k: k*2)
	assert d['as'] == 'asas'
