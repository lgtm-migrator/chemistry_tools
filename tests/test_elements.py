# 3rd party
import pytest  # type: ignore

# this package
from chemistry_tools.elements import ELEMENTS, H, Isotope, groups


@pytest.mark.parametrize(
		"massnumber, symbol",
		[
				(1, "H"),
				(4, "He"),
				(7, "Li"),
				(9, "Be"),
				(11, "B"),
				(12, "C"),
				(14, "N"),
				(16, "O"),
				(19, "F"),
				(20, "Ne"),
				(23, "Na"),
				(24, "Mg"),
				(27, "Al"),
				(28, "Si"),
				(31, "P"),
				(32, "S"),
				(35, "Cl"),
				(40, "Ar"),
				(39, "K"),
				(40, "Ca"),
				(45, "Sc"),
				(48, "Ti"),
				(51, "V"),
				(52, "Cr"),
				(55, "Mn"),
				(56, "Fe"),
				(59, "Co"),
				(58, "Ni"),
				(63, "Cu"),
				(64, "Zn"),
				(69, "Ga"),
				(74, "Ge"),
				(75, "As"),
				(80, "Se"),
				(79, "Br"),
				(84, "Kr"),
				(85, "Rb"),
				(88, "Sr"),
				(89, "Y"),
				(90, "Zr"),
				(93, "Nb"),
				(98, "Mo"),
				(102, "Ru"),
				(103, "Rh"),
				(106, "Pd"),
				(107, "Ag"),
				(114, "Cd"),
				(115, "In"),
				(120, "Sn"),
				(121, "Sb"),
				(130, "Te"),
				(127, "I"),
				(132, "Xe"),
				(133, "Cs"),
				(138, "Ba"),
				(139, "La"),
				(140, "Ce"),
				(141, "Pr"),
				(142, "Nd"),
				(152, "Sm"),
				(153, "Eu"),
				(158, "Gd"),
				(159, "Tb"),
				(164, "Dy"),
				(165, "Ho"),
				(166, "Er"),
				(169, "Tm"),
				(174, "Yb"),
				(175, "Lu"),
				(180, "Hf"),
				(181, "Ta"),
				(184, "W"),
				(187, "Re"),
				(192, "Os"),
				(193, "Ir"),
				(195, "Pt"),
				(197, "Au"),
				(202, "Hg"),
				(205, "Tl"),
				(208, "Pb"),
				(209, "Bi"),
				(232, "Th"),
				(238, "U"),
				]
		)
def test_isotopes(symbol, massnumber):
	element = ELEMENTS[symbol]

	max_abundance_massnumber = 0
	max_isotope_abundance = 0

	for isotope in element.isotopes.values():
		if isotope.abundance > max_isotope_abundance:
			max_isotope_abundance = isotope.abundance
			max_abundance_massnumber = isotope.massnumber

	assert max_abundance_massnumber == massnumber


def test_hydrogen():
	assert str(ELEMENTS[1]) == "Hydrogen"
	repr(ELEMENTS[1])

	assert (ELEMENTS["H"] == ELEMENTS["Hydrogen"])
	assert (ELEMENTS["H"] == ELEMENTS["hydrogen"])
	assert (ELEMENTS["H"] == ELEMENTS["hydrOgen"])
	assert (ELEMENTS["H"] != ELEMENTS[2])

	assert ELEMENTS["H"].number == 1
	assert ELEMENTS["H"].symbol == "H"
	assert ELEMENTS["H"].name == "Hydrogen"

	assert ELEMENTS["H"].electrons == ELEMENTS["H"].number
	assert ELEMENTS["H"].protons == ELEMENTS["H"].number

	assert ELEMENTS["H"].group == 1
	assert ELEMENTS["H"].period == 1
	assert ELEMENTS["H"].block == "s"
	assert ELEMENTS["H"].series == 1

	assert ELEMENTS["H"].mass == 1.007941
	assert ELEMENTS["H"].eleneg == 2.2
	assert ELEMENTS["H"].eleaffin == 0.75420375
	assert ELEMENTS["H"].covrad == 0.32
	assert ELEMENTS["H"].atmrad == 0.79
	assert ELEMENTS["H"].vdwrad == 1.2
	assert ELEMENTS["H"].tboil == 20.28
	assert ELEMENTS["H"].tmelt == 13.81

	assert ELEMENTS["H"].density == 0.084
	assert ELEMENTS["H"].eleconfig == '1s'
	assert ELEMENTS["H"].oxistates == '1*, -1'
	assert ELEMENTS["H"].ionenergy == (13.5984, )

	assert ELEMENTS["H"].isotopes == {
			1: Isotope(1.00782503207, 0.999885, 1),
			2: Isotope(2.0141017778, 0.000115, 2),
			3: Isotope(3.0160492777, 0.0, 3),
			4: Isotope(4.02781, 0.0, 4),
			5: Isotope(5.03531, 0.0, 5),
			6: Isotope(6.04494, 0.0, 6),
			7: Isotope(7.05275, 0.0, 7),
			}

	repr(ELEMENTS[1:10:2])

	assert ELEMENTS["Hydrogen"] == ELEMENTS["H"]
	assert ELEMENTS["Hydrogen"] == ELEMENTS["hydrogen"]
	assert ELEMENTS["Hydrogen"] == ELEMENTS["hydrOgen"]
	assert ELEMENTS["Hydrogen"] == ELEMENTS["HydrOgen"]
	assert ELEMENTS["Hydrogen"] == H

	assert ELEMENTS["H"].description == (
			"Colourless, odourless gaseous chemical element. Lightest and most "
			"abundant element in the universe. Present in water and in all "
			"organic compounds. Chemically reacts with most elements. Discovered "
			"by Henry Cavendish in 1776."
			)


def test_groups():
	assert groups[1] == (1, 3, 11, 19, 37, 55, 87)
	assert groups[2] == (4, 12, 20, 38, 56, 88)
	assert groups[13] == (5, 13, 31, 49, 81, 113)
	assert groups[14] == (6, 14, 32, 50, 82, 114)
	assert groups[15] == (7, 15, 33, 51, 83, 115)
	assert groups[16] == (8, 16, 34, 52, 84, 116)
	assert groups[17] == (9, 17, 35, 53, 85, 117)
	assert groups[18] == (2, 10, 18, 36, 54, 86, 118)


def test_atomic_number():
	assert ELEMENTS['U'].number == 92
	assert ELEMENTS['carbon'].number == 6
	assert ELEMENTS['moscovium'].number == 115
	with pytest.raises(KeyError):
		ELEMENTS['unobtainium']
