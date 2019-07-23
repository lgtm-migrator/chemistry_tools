# -*- coding: utf-8 -*-
"""
test_property_format
~~~~~~~~~~~~~

Test property_format

"""


import pytest

from chemistry_tools import PropertyFormat

def test_degC():
	assert PropertyFormat.degC("150 deg C") == "150°C"
	assert PropertyFormat.degC("150deg C") == "150°C"
	assert PropertyFormat.degC("150 DEG C") == "150°C"
	assert PropertyFormat.degC("150DEG C") == "150°C"
	
def test_equals():
	assert PropertyFormat.equals("Val= 1234") == "Val = 1234"
	assert PropertyFormat.equals("Val = 1234") == "Val = 1234"
	
#def test_scientific():
#	assert PropertyFormat.scientific("123x108")

def test_uscg1999():
	assert PropertyFormat.uscg1999("1234(USCG, 1999)") == '1234'

def test_trailspace():
	assert PropertyFormat.trailspace("1234     ") == "1234"

def test_f2c():
	assert PropertyFormat.f2c("32°F") == "0E-28°C"
	# TODO: Fix
