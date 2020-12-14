# this package
from chemistry_tools.property_format import degC, equals, f2c, uscg1999


def test_degC():
	assert degC("150 deg C") == "150 °C"
	assert degC("150deg C") == "150 °C"
	assert degC("150 DEG C") == "150 °C"
	assert degC("150DEG C") == "150 °C"


def test_equals():
	assert equals("Val= 1234") == "Val = 1234"
	assert equals("Val = 1234") == "Val = 1234"


# def test_scientific():
# 	assert PropertyFormat.scientific("123x108")


def test_uscg1999():
	assert uscg1999("1234(USCG, 1999)") == "1234"


def test_f2c():
	assert f2c("32°F") == "0E-28°C"
