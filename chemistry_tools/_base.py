#!/usr/bin/env python3
#
#  _base.py
"""
Base class
"""
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

from abc import ABC, abstractmethod


class ChemToolsBase(ABC):
	@abstractmethod
	def __init__(self, *args, **kwargs):
		pass
	
	def __str__(self):
		return self.__repr__()
	
	def __iter__(self):
		for key, value in self.__dict__().items():
			yield key, value
	
	def __getstate__(self):
		return self.__dict__()
	
	def __setstate__(self, state):
		self.__init__(**state)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		return self.__copy__()
	
	@abstractmethod
	def __dict__(self):
		return dict()
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__() == other.__dict__()
		
		return NotImplemented
