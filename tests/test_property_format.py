# this package
from chemistry_tools import property_format


def test_degC():
	assert property_format.degC("150 deg C") == "150 °C"
	assert property_format.degC("150deg C") == "150 °C"
	assert property_format.degC("150 DEG C") == "150 °C"
	assert property_format.degC("150DEG C") == "150 °C"


def test_equals():
	assert property_format.equals("Val= 1234") == "Val = 1234"
	assert property_format.equals("Val = 1234") == "Val = 1234"


# def test_scientific():
# 	assert PropertyFormat.scientific("123x108")


def test_uscg1999():
	assert property_format.uscg1999("1234(USCG, 1999)") == "1234"


def test_trailspace():
	assert property_format.trailspace("1234     ") == "1234"


def test_f2c():
	assert property_format.f2c("32°F") == "0E-28°C"


# TODO: Fix
