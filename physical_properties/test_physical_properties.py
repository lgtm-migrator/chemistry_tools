# 3rd party
import pytest

# this package
from chemistry_tools.pubchem.compound import Compound


@pytest.fixture(scope="module")
def c1():
	"""Compound CID 241."""
	return Compound.from_cid(241)


@pytest.fixture(scope="module")
def c2():
	"""Compound CID 175."""
	return Compound.from_cid(175)


def test_properties_types(c1):
	# assert isinstance(c1.boiling_point, Decimal)
	# TODO: Boiling point now returns string
	# TODO:	assert c1.boiling_point == '80.11111111111111111111111112°C at 760 mm Hg (NTP, 1992)'
	# TODO:assert isinstance(c1.color, str)
	# TODO:assert isinstance(c1.density, str)
	# TODO:assert isinstance(c1.specific_gravity, str)
	# assert isinstance(c1.dissociation_constant, )
	# TODO
	# TODO:assert isinstance(c1.heat_combustion, str)
	# assert isinstance(c1.melting_point, Decimal)
	# TODO:assert c1.melting_point == '5.5°C (NTP, 1992)'
	# TODO: melting point now returns string

	# TODO:assert isinstance(c1.partition_coeff, str)
	# TODO:assert isinstance(c1.odor, str)
	# TODO:assert isinstance(c1.other_props, str)
	# TODO:assert isinstance(c1.solubility, str)
	# TODO:assert isinstance(c1.spectral_props, str)
	# TODO:assert isinstance(c1.surface_tension, str)
	# TODO:assert isinstance(c1.vapor_density, str)
	# TODO:assert isinstance(c1.vapor_pressure, str)
	# TODO:assert isinstance(c1.full_record, dict)

	pass


def test_values(c1):
	# TODO: Now seems to return formatted string
	# assert c1.boiling_point == Decimal('80.08')
	# TODO:assert c1.boiling_point == "80.11111111111111111111111112°C at 760 mm Hg (NTP, 1992)"
	# TODO:assert c1.color == 'Clear, colorless liquid'
	# TODO:assert c1.density == '0.879 at 20°C'
	# TODO:assert c1.specific_gravity == '0.879 at 20°C'
	# TODO: What happened to the units (g/cu cm) for density and specific gravity?
	# assert c1.dissociation_constant ==
	# TODO
	# TODO:assert c1.heat_combustion == '-3267.6 kJ/mol (liquid)'
	# assert c1.melting_point == Decimal('5.558')
	# TODO:assert c1.melting_point == "5.5°C (NTP, 1992)"
	# assert c1.partition_coeff == 'log Kow = 2.13'
	# TODO:assert c1.partition_coeff == '2.13 (LogP)'
	# TODO:assert c1.odor == 'Aromatic odor'
	# TODO:assert c1.other_props == 'Conversion factors: 1 mg/cu m = 0.31 ppm; 1 ppm = 3.26 mg/cu m'
	# assert c1.solubility == 'In water, 1.79×10<sup>+3</sup> mg/L at 25°C'
	# assert c1.spectral_props == 'MAX ABSORPTION (ALCOHOL): 243 NM (LOG E = 2.2), 249 NM (LOG E = 2.3), 256 NM (LOG E = 2.4), 261 NM (LOG E = 2.2); SADTLER REF NUMBER: 6402 (IR, PRISM), 1765 (UV)'
	# TODO:assert c1.surface_tension == '28.22 mN/m at 25 °C'
	# assert c1.vapor_density == '2.8 (Air = 1)'
	# assert c1.vapor_pressure == '94.8 mm Hg at 25 °C'
	# TODO: Sort out solubility, spectral_props, vapor_density, vapor_pressure
	pass


def test_get_property(c1):
	assert isinstance(c1.get_property("Melting Point"), dict)
	# TODO: Record for Benzene now seems to return a string with markup, not a number
	# assert isinstance(c1.get_property_value("Melting Point"), Decimal)
	# assert c1.get_property_value("Melting Point") == Decimal('5.558')
	assert isinstance(c1.get_property_value("Melting Point"), str)
	assert c1.get_property_value("Melting Point") == "5.5°C (NTP, 1992)"
	assert c1.melting_point == c1.get_property_value("Melting Point")
	assert isinstance(c1.get_property_description("Melting Point"), str)
	# assert c1.get_property_description("Melting Point") is None
	# assert isinstance(c1.get_property_unit("Melting Point"), str)
	assert c1.get_property_unit("Melting Point") is None

	assert isinstance(c1.get_property("Boiling Point"), dict)
	assert isinstance(c1.get_property("Heat Combustion"), dict)
	assert isinstance(c1.get_property("Exact Mass"), dict)
