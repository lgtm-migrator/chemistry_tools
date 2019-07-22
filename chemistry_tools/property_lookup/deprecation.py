#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  deprecation.py
#  Based on PubChemPy by Matt Swain <m.swain@me.com>
#  Available under the MIT License
#
#  Copyright (c) 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
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

import warnings
import functools


def deprecated(message=None):
	"""Decorator to mark functions as deprecated. A warning will be emitted when the function is used."""
	
	def deco(func):
		@functools.wraps(func)
		def wrapped(*args, **kwargs):
			warnings.warn(
				message or 'Call to deprecated function {}'.format(func.__name__),
				category=PubChemPyDeprecationWarning,
				stacklevel=2
			)
			return func(*args, **kwargs)
		
		return wrapped
	
	return deco


class PubChemPyDeprecationWarning(Warning):
	"""Warning category for deprecated features."""
	pass
