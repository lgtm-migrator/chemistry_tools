#!/usr/bin/env python3
#
#  test_utils.py
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

from chemistry_tools.utils import defaultnamedtuple


def test_defaultnamedtuple():
	Point2 = defaultnamedtuple('Point2', 'x y', [10])
	p = Point2(3)
	assert p.x == 3 and p.y == 10
	
	Point3 = defaultnamedtuple('Point3', 'x y z', [10, 20])
	p = Point3(3)
	assert p.x == 3 and p.y == 10 and p.z == 20
	
	p = Point3(3, z=30)
	assert p.x == 3 and p.y == 10 and p.z == 30
	
	p = Point3(3, 4, 5)
	assert p.x == 3 and p.y == 4 and p.z == 5
	
	_default_y = Point2.__new__.__defaults__[-1]
	
	class MySubclass(Point2):
		
		def __new__(cls, x2, y2=_default_y):
			return super().__new__(cls, x2**.5, y2**.5)
	
	p2 = MySubclass(9, 4)
	assert isinstance(p2, tuple)
	assert isinstance(p2, Point2)
	assert isinstance(p2, MySubclass)
	assert not isinstance(p, MySubclass)
	assert p2.x == 3
	assert p2.y == 2
	
	p3 = MySubclass(9)
	assert p3.x == 3
	assert p3.y == 10**.5

