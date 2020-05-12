#!/usr/bin/env python3
#
#  test_chemistry.py
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

# stdlib
from functools import reduce
from operator import add, attrgetter

# 3rd party
import pytest

# this package
from chempy.chemistry import (balance_stoichiometry, Equilibrium, equilibrium_quotient, Reaction, Species, Substance)
from chemistry_tools.units import allclose, to_unitless
from chemistry_tools import units
from chemistry_tools.dicts import ArithmeticDict
import quantities


def test_equilibrium_quotient():
	assert abs(equilibrium_quotient([2.3, 3.7, 5.1], (-1, -1, 1)) - 5.1 / 2.3 / 3.7) < 1e-14


def test_Reaction():
	substances = s_Hp, s_OHm, s_H2O = (
			Substance('H+', composition={0: 1, 1: 1}),
			Substance('OH-', composition={0: -1, 1: 1, 8: 1}),
			Substance('H2O', composition={0: 0, 1: 2, 8: 1}),
			)
	substance_names = Hp, OHm, H2O = [s.name for s in substances]
	substance_dict = {n: s for n, s in zip(substance_names, substances)}
	r1 = Reaction({Hp: 1, OHm: 1}, {H2O: 1})
	assert sum(r1.composition_violation(substance_dict)) == 0
	assert r1.composition_violation(substance_dict, ['H+']) == [0]
	viol, cks = r1.composition_violation(substance_dict, True)
	assert viol == [0] * 3 and sorted(cks) == [0, 1, 8]
	assert r1.charge_neutrality_violation(substance_dict) == 0
	
	r2 = Reaction({Hp: 1, OHm: 1}, {H2O: 2})
	assert sum(r2.composition_violation(substance_dict)) != 0
	assert r2.charge_neutrality_violation(substance_dict) == 0
	
	r3 = Reaction({Hp: 2, OHm: 1}, {H2O: 2})
	assert sum(r3.composition_violation(substance_dict)) != 0
	assert r3.charge_neutrality_violation(substance_dict) != 0
	assert r3.keys() == {Hp, OHm, H2O}
	
	with pytest.raises(ValueError):
		Reaction({Hp: -1, OHm: -1}, {H2O: -1})
	
	assert r1 == Reaction({'H+', 'OH-'}, {'H2O'})
	
	r4 = Reaction({Hp, OHm}, {H2O}, 7)
	ref = {Hp: -3 * 5 * 7, OHm: -3 * 5 * 7, H2O: 3 * 5 * 7}
	
	r5 = r4.copy()
	assert r5 == r4
	assert r5 != r1
	
	lhs5, rhs5 = {'H+': 1, 'OH-': 1}, {'H2O': 1}
	r5 = Reaction(lhs5, rhs5)
	assert r5.reac == lhs5 and r5.prod == rhs5


def test_Reaction__copy():
	r1 = Reaction({'H2O'}, {'H2O'}, checks=())
	r2 = r1.copy()
	assert r1 == r2
	r2.reac['H2O2'] = r2.reac.pop('H2O')  # 1
	r2.prod['H2O2'] = r2.prod.pop('H2O')  # 1
	assert r1.reac == {'H2O': 1} and r1.prod == {'H2O': 1}


def test_Reaction__from_string():

	
	r = Reaction.from_string("H2O -> H+ + OH-; 1e-4", 'H2O H+ OH-'.split())
	assert r.reac == {'H2O': 1} and r.prod == {'H+': 1, 'OH-': 1}
	
	with pytest.raises(ValueError):
		Reaction.from_string("H2O -> H+ + OH-; 1e-4", 'H2O H OH-'.split())
	
	r2 = Reaction.from_string("H2O -> H+ + OH-; 1e-4; ref='important_paper'")
	assert r2.ref == 'important_paper'
	
	with pytest.raises(ValueError):
		Reaction.from_string("H2O -> H2O")
	Reaction.from_string("H2O -> H2O; None; checks=()")
	
	with pytest.raises(ValueError):
		Reaction({'H2O': 2}, {'H2O2': 2, 'O2': -2})
	
	r4 = Reaction({'H+': 2, 'OH-': 1}, {'H2O': 2}, 42.0)
	assert Reaction.from_string(str(r4), 'H+ OH- H2O') == r4
	assert Reaction.from_string(str(r4), None) == r4
	
	r5 = Reaction.from_string("H2O2 -> 0.5 O2 + H2O", checks=[
			c for c in Reaction.default_checks if c != 'all_integral'])
	r6 = r5.copy()
	assert r5 == r6
	
	r7 = Reaction.from_string("H2O -> H + OH; None; data=dict(ref='foo; bar; baz;')  # foobar")
	assert r7.data['ref'] == 'foo; bar; baz;'


@pytest.mark.skip
def test_Reaction_from_string__units():

	
	r5 = Reaction.from_string('2 H2O2 -> O2 + 2 H2O; 1e-7/molar/second', 'H2O O2 H2O2')
	assert to_unitless(r5.param, 1 / quantities.molar / quantities.second) == 1e-7
	r6 = Reaction.from_string('->', checks=())
	assert r6.reac == {} and r6.prod == {}
	
	r7 = Reaction.from_string('2 A -> B; exp(log(2e-3))*metre**3/mol/hour', None)
	assert r7.reac == {'A': 2} and r7.prod == {'B': 1}
	assert allclose(r7.param, 2e-3 * units.m3 / quantities.mol / quantities.hour)
	
	with pytest.raises(ValueError):
		Reaction.from_string('2 A -> B; 2e-3/hour', None)
	
	r8 = Reaction.from_string('A -> B; "k"')
	
	r9 = Reaction.from_string('A -> B; 42.0')
	
	Reaction.from_string("H+ + OH- -> H2O; 1e10/M/s", 'H2O H+ OH-'.split())
	with pytest.raises(ValueError):
		Reaction.from_string("H2O -> H+ + OH-; 1e-4/M/s", 'H2O H+ OH-'.split())


def test_Equilibrium__as_reactions():

	
	s = quantities.second
	M = quantities.molar
	H2O, Hp, OHm = map(Substance, 'H2O H+ OH-'.split())
	eq = Equilibrium({'H2O': 1}, {'H+': 1, 'OH-': 1}, 1e-14)
	rate = 1.31e11 / M / s
	fw, bw = eq.as_reactions(kb=rate, units=quantities)
	assert abs((bw.param - rate) / rate) < 1e-15
	assert abs((fw.param / M) / bw.param - 1e-14) / 1e-14 < 1e-15


def test_ReactioN__latex():

	keys = 'H2O H2 O2'.split()
	subst = {k: Substance.from_formula(k) for k in keys}
	r2 = Reaction.from_string("2 H2O -> 2 H2 + O2", subst)
	assert r2.latex(subst) == r'2 H_{2}O \rightarrow 2 H_{2} + O_{2}'
	r3 = Reaction.from_string("2 H2O -> 2 H2 + O2; 42; name='split'", subst)
	assert r3.latex(subst, with_param=True, with_name=True) == r'2 H_{2}O \rightarrow 2 H_{2} + O_{2}; 42; split'
	assert r3.latex(subst, with_name=True) == r'2 H_{2}O \rightarrow 2 H_{2} + O_{2}; split'
	assert r3.latex(subst, with_param=True) == r'2 H_{2}O \rightarrow 2 H_{2} + O_{2}; 42'
	assert r3.latex(subst) == r'2 H_{2}O \rightarrow 2 H_{2} + O_{2}'


def test_Reaction__unicode():
	
	keys = 'H2O H2 O2'.split()
	subst = {k: Substance.from_formula(k) for k in keys}
	r2 = Reaction.from_string("2 H2O -> 2 H2 + O2", subst)
	assert r2.unicode(subst) == '2 H₂O → 2 H₂ + O₂'
	r3 = Reaction.from_string("2 H2O -> 2 H2 + O2; 42; name='split'", subst)
	assert r3.unicode(subst) == '2 H₂O → 2 H₂ + O₂'
	assert r3.unicode(subst, with_name=True) == '2 H₂O → 2 H₂ + O₂; split'
	assert r3.unicode(subst, with_name=True, with_param=True) == '2 H₂O → 2 H₂ + O₂; 42; split'
	assert r3.unicode(subst, with_param=True) == '2 H₂O → 2 H₂ + O₂; 42'


def test_Reaction__html():
	
	keys = 'H2O H2 O2'.split()
	subst = {k: Substance.from_formula(k) for k in keys}
	r2 = Reaction.from_string("2 H2O -> 2 H2 + O2", subst)
	assert r2.html(subst) == '2 H<sub>2</sub>O &rarr; 2 H<sub>2</sub> + O<sub>2</sub>'
	assert r2.html(subst, Reaction_coeff_fmt=lambda s: f'<b>{s}</b>') == \
		   '<b>2</b> H<sub>2</sub>O &rarr; <b>2</b> H<sub>2</sub> + O<sub>2</sub>'
	assert r2.html(subst, Reaction_formula_fmt=lambda s: f'<b>{s}</b>') == \
		   '2 <b>H<sub>2</sub>O</b> &rarr; 2 <b>H<sub>2</sub></b> + <b>O<sub>2</sub></b>'


def test_Reaction__idempotency():
	with pytest.raises(ValueError):
		Reaction({'A': 1}, {'A': 1})
	with pytest.raises(ValueError):
		Reaction({}, {})
	with pytest.raises(ValueError):
		Reaction({'A': 1}, {'B': 1}, inact_reac={'B': 1}, inact_prod={'A': 1})


def test_Equilibrium__eliminate():
	sympy = pytest.importorskip("sympy")
	
	e1 = Equilibrium({'A': 1, 'B': 2}, {'C': 3})
	e2 = Equilibrium({'D': 5, 'B': 7}, {'E': 11})
	coeff = Equilibrium.eliminate([e1, e2], 'B')
	assert coeff == [7, -2]
	
	e3 = coeff[0] * e1 + coeff[1] * e2
	assert e3.net_stoich('B') == (0,)
	
	e4 = e1 * coeff[0] + coeff[1] * e2
	assert e4.net_stoich('B') == (0,)
	
	assert (-e1).reac == {'C': 3}
	assert (e2 * -3).reac == {'E': 33}


@pytest.mark.xfail
def test_Equilibrium__from_string():

	assert Equilibrium.from_string('H2O = H+ + OH-').param is None
	assert Equilibrium.from_string('H2O = H+ + OH-; 1e-14').param == 1e-14
	assert Equilibrium.from_string('H2O = H+ + OH-; 1e-14*molar').param ** 0 == 1
	with pytest.raises(ValueError):
		Equilibrium.from_string('H+ + OH- = H2O; 1e-14*molar')


def test_Equilibrium__cancel():
	# 2B + C -> E
	e1 = Equilibrium({'A': 26, 'B': 20, 'C': 7}, {'D': 4, 'E': 7})
	e2 = Equilibrium({'A': 13, 'B': 3}, {'D': 2})
	coeff = e1.cancel(e2)
	assert coeff == -2


def test_balance_stoichiometry():
	sympy = pytest.importorskip("sympy")
	
	# 4 NH4ClO4 -> 2 N2 + 4 HCl + 6H2O + 5O2
	# 4 Al + 3O2 -> 2Al2O3
	# ---------------------------------------
	# 6 NH4ClO4 + 10 Al + -> 3 N2 + 6 HCl + 9 H2O + 5 Al2O3
	reac, prod = balance_stoichiometry({'NH4ClO4', 'Al'}, {'Al2O3', 'HCl', 'H2O', 'N2'})
	assert reac == {'NH4ClO4': 6, 'Al': 10}
	assert prod == {'Al2O3': 5, 'HCl': 6, 'H2O': 9, 'N2': 3}
	
	r3, p3 = balance_stoichiometry({'C2H6', 'O2'}, {'H2O', 'CO2'})
	assert r3 == {'C2H6': 2, 'O2': 7}
	assert p3 == {'CO2': 4, 'H2O': 6}
	
	r4, p4 = balance_stoichiometry({'C7H5(NO2)3', 'NH4NO3'}, {'CO', 'H2O', 'N2'})
	assert r4 == {'C7H5(NO2)3': 2, 'NH4NO3': 7}
	assert p4 == {'CO': 14, 'H2O': 19, 'N2': 10}
	
	a5, b5 = {"C3H5NO", "CH4", "NH3", "H2O"}, {"C2H6", "CH4O", "CH5N", "CH3N"}
	formulas = list(set.union(a5, b5))
	substances = dict(zip(formulas, map(Substance.from_formula, formulas)))
	compositions = {k: ArithmeticDict(int, substances[k].composition) for k in formulas}
	r5, p5 = balance_stoichiometry(a5, b5)
	compo_reac = dict(reduce(add, [compositions[k] * v for k, v in r5.items()]))
	compo_prod = dict(reduce(add, [compositions[k] * v for k, v in p5.items()]))
	assert compo_reac == compo_prod
	
	a6, b6 = map(lambda x: set(x.split()), 'CuSCN KIO3 HCl;CuSO4 KCl HCN ICl H2O'.split(';'))
	r6, p6 = balance_stoichiometry(a6, b6)
	assert r6 == dict(CuSCN=4, KIO3=7, HCl=14)
	assert p6 == dict(CuSO4=4, KCl=7, HCN=4, ICl=7, H2O=5)
	
	r7, p7 = balance_stoichiometry({'Zn+2', 'e-'}, {'Zn'})
	assert r7 == {'Zn+2': 1, 'e-': 2}
	assert p7 == {'Zn': 1}
	
	r8, p8 = balance_stoichiometry({'Zn'}, {'Zn+2', 'e-'})
	assert r8 == {'Zn': 1}
	assert p8 == {'Zn+2': 1, 'e-': 2}


def test_balance_stoichiometry__ordering():
	sympy = pytest.importorskip("sympy")
	
	reac, prod = 'CuSCN KIO3 HCl'.split(), 'CuSO4 KCl HCN ICl H2O'.split()
	rxn = Reaction(*balance_stoichiometry(reac, prod))
	res = rxn.string()
	ref = '4 CuSCN + 7 KIO3 + 14 HCl -> 4 CuSO4 + 7 KCl + 4 HCN + 7 ICl + 5 H2O'
	assert res == ref


def test_balance_stoichiometry__simple():
	sympy = pytest.importorskip("sympy")
	
	r2, p2 = balance_stoichiometry({'Na2CO3'}, {'Na2O', 'CO2'})
	assert r2 == {'Na2CO3': 1}
	assert p2 == {'Na2O': 1, 'CO2': 1}


@pytest.mark.parametrize('underdet', [False, None, True])
def test_balance_stoichiometry__impossible(underdet):
	sympy = pytest.importorskip("sympy")
	
	from pulp import PulpSolverError
	with pytest.raises((ValueError, PulpSolverError)):
		r1, p1 = balance_stoichiometry({'CO'}, {'CO2'}, underdetermined=underdet)


def test_balance_stoichiometry__underdetermined():
	sympy = pytest.importorskip("sympy")
	pulp = pytest.importorskip("pulp")
	
	from pulp import PulpSolverError
	
	with pytest.raises(ValueError):
		balance_stoichiometry({'C2H6', 'O2'}, {'H2O', 'CO2', 'CO'}, underdetermined=False)
	reac, prod = balance_stoichiometry({'C2H6', 'O2'}, {'H2O', 'CO2', 'CO'})
	
	r1 = {'C7H5O3-', 'O2', 'C21H27N7O14P2-2', 'H+'}
	p1 = {'C7H5O4-', 'C21H26N7O14P2-', 'H2O'}  # see https://github.com/bjodah/chempy/issues/67
	bal1 = balance_stoichiometry(r1, p1, underdetermined=None)
	assert bal1 == ({'C21H27N7O14P2-2': 1, 'H+': 1, 'C7H5O3-': 1, 'O2': 1},
					{'C21H26N7O14P2-': 1, 'H2O': 1, 'C7H5O4-': 1})
	
	with pytest.raises(ValueError):
		balance_stoichiometry({'C3H4O3', 'H3PO4'}, {'C3H6O3'}, underdetermined=None)
	
	for underdet in [False, True, None]:
		with pytest.raises((ValueError, PulpSolverError)):
			balance_stoichiometry({'C3H6O3'}, {'C3H4O3'}, underdetermined=underdet)
	
	with pytest.raises(ValueError):  # https://github.com/bjodah/chempy/pull/86#issuecomment-375421609
		balance_stoichiometry({'C21H36N7O16P3S', 'C3H4O3'}, {'H2O', 'C5H8O3', 'C24H38N7O18P3S'})


def test_balance_stoichiometry__very_underdetermined():
	sympy = pytest.importorskip("sympy")
	pulp = pytest.importorskip("pulp")
	
	r3 = set('O2 Fe Al Cr'.split())
	p3 = set('FeO Fe2O3 Fe3O4 Al2O3 Cr2O3 CrO3'.split())
	bal3 = balance_stoichiometry(r3, p3, underdetermined=None)
	ref3 = {'Fe': 7, 'Al': 2, 'Cr': 3, 'O2': 9}, {k: 2 if k == 'FeO' else 1 for k in p3}
	substances = {k: Substance.from_formula(k) for k in r3 | p3}
	assert all(viol == 0 for viol in Reaction(*ref3).composition_violation(substances))
	assert sum(bal3[0].values()) + sum(bal3[1].values()) <= sum(ref3[0].values()) + sum(ref3[1].values())
	assert bal3 == ref3


def test_balance_stoichiometry__underdetermined__canoncial():
	sympy = pytest.importorskip("sympy")
	pulp = pytest.importorskip("pulp")
	
	# This tests for canoncial representation of the underdetermined system
	# where all coefficients are integer and >= 1. It is however of limited
	# practical use (and hence marked ``xfail``) since underdetermined systems
	# have infinite number of solutions. It should however be possible to rewrite
	# the logic so that such canoncial results are returned from balance_stoichiometry
	r2 = {'O2', 'O3', 'C', 'NO', 'N2O', 'NO2', 'N2O4'}
	p2 = {'CO', 'CO2', 'N2'}
	bal2 = balance_stoichiometry(r2, p2, underdetermined=None)
	ref2 = ({'O2': 1, 'O3': 1, 'C': 7, 'NO': 1, 'N2O': 1, 'NO2': 1, 'N2O4': 1},
			{'CO': 1, 'CO2': 6, 'N2': 3})
	substances = {k: Substance.from_formula(k) for k in r2 | p2}
	assert all(viol == 0 for viol in Reaction(*ref2).composition_violation(substances))
	assert sum(bal2[0].values()) + sum(bal2[1].values()) <= sum(ref2[0].values()) + sum(ref2[1].values())
	assert bal2 == ref2


def test_balance_stoichiometry__substances__underdetermined():
	sympy = pytest.importorskip("sympy")
	pulp = pytest.importorskip("pulp")
	
	substances = {s.name: s for s in [
			Substance('eggs_6pack', composition=dict(eggs=6)),
			Substance('milk_carton', composition=dict(cups_of_milk=4)),
			Substance('flour_bag', composition=dict(spoons_of_flour=30)),
			Substance('pancake', composition=dict(eggs=1, cups_of_milk=1, spoons_of_flour=2)),
			Substance('waffle', composition=dict(eggs=2, cups_of_milk=2, spoons_of_flour=3)),
			]}
	ur1 = {'eggs_6pack', 'milk_carton', 'flour_bag'}
	up1 = {'pancake', 'waffle'}
	br1, bp1 = balance_stoichiometry(ur1, up1, substances=substances, underdetermined=None)
	ref_r1 = {'eggs_6pack': 6, 'flour_bag': 2, 'milk_carton': 9}
	ref_p1 = {'pancake': 12, 'waffle': 12}
	assert all(viol == 0 for viol in Reaction(ref_r1, ref_p1).composition_violation(substances))
	assert all(v > 0 for v in br1.values()) and all(v > 0 for v in bp1.values())
	assert bp1 == ref_p1
	assert br1 == ref_r1


def test_balance_stoichiometry__missing_product_atom():
	sympy = pytest.importorskip("sympy")
	
	with pytest.raises(ValueError):  # No Al on product side
		balance_stoichiometry({'C7H5(NO2)3', 'Al', 'NH4NO3'}, {'CO', 'H2O', 'N2'})


def test_balance_stoichiometry__duplicates():
	sympy = pytest.importorskip("sympy")
	
	cases = """
C + CO + CO2 -> C + CO        # suggested solution:  C +      CO2 ->     2 CO
C + CO + CO2 -> C +      CO2  # suggested solution:      2 CO      -> C +      CO2
C + CO + CO2 ->     CO + CO2  # suggested solution:  C +      CO2 ->     2 CO
C + CO       -> C + CO + CO2  # suggested solution:      2 CO      -> C +      CO2
C +      CO2 -> C + CO + CO2  # suggested solution:  C +      CO2 ->     2 CO
    CO + CO2 -> C + CO + CO2  # suggested solution:      2 CO      -> C +      CO2
"""
	for prob, sol in [l.split('#') for l in cases.strip().splitlines()]:
		tst_r = Reaction.from_string(prob)
		ref_r = Reaction.from_string(sol.split(':')[1])
		tst_bal = balance_stoichiometry(tst_r.reac, tst_r.prod,
										allow_duplicates=True, underdetermined=None)
		assert Reaction(*tst_bal) == ref_r
	
	with pytest.raises(ValueError):
		balance_stoichiometry({'C', 'CO', 'CO2'}, {'C', 'CO', 'CO2'},
							  allow_duplicates=True, underdetermined=None)
	
	gh120 = {'H4P2O7', 'HPO3', 'H2O'}, {'H4P2O7', 'HPO3'}
	bal120 = balance_stoichiometry(*gh120, allow_duplicates=True, underdetermined=None)
	assert bal120 == ({'HPO3': 2, 'H2O': 1}, {'H4P2O7': 1})
	
	with pytest.raises(ValueError):
		balance_stoichiometry(*gh120)
	
	# https://github.com/bjodah/chempy/issues/120#issuecomment-434453703
	bal_Mn = balance_stoichiometry({'H2O2', 'Mn1', 'H1'}, {'Mn1', 'H2O1'}, allow_duplicates=True, underdetermined=None)
	assert bal_Mn == ({'H2O2': 1, 'H1': 2}, {'H2O1': 2})
	
	bal_Mn_COx = balance_stoichiometry({'C', 'CO', 'CO2', 'Mn'}, {'C', 'CO2', 'Mn'},
									   allow_duplicates=True, underdetermined=None)
	assert bal_Mn_COx == ({'CO': 2}, {'C': 1, 'CO2': 1})


def test_to_reaction():
	from chempy.chemistry import Reaction, Equilibrium
	rxn = to_reaction(
			"H+ + OH- -> H2O; 1.4e11; ref={'doi': '10.1039/FT9908601539'}",
			'H+ OH- H2O'.split(), '->', Reaction)
	assert rxn.__class__ == Reaction
	
	assert rxn.reac['H+'] == 1
	assert rxn.reac['OH-'] == 1
	assert rxn.prod['H2O'] == 1
	assert rxn.param == 1.4e11
	assert rxn.ref['doi'].startswith('10.')
	
	eq = to_reaction("H+ + OH- = H2O; 1e-14; ref='rt, [H2O] == 1 M'",
					 'H+ OH- H2O'.split(), '=', Equilibrium)
	assert eq.__class__ == Equilibrium
	
	assert eq.reac['H+'] == 1
	assert eq.reac['OH-'] == 1
	assert eq.prod['H2O'] == 1
	assert eq.ref.startswith('rt')
	
	for s in ['2 e-(aq) + (2 H2O) -> H2 + 2 OH- ; 1e6 ; ',
			  '2 * e-(aq) + (2 H2O) -> 1 * H2 + 2 * OH- ; 1e6 ; ']:
		rxn2 = to_reaction(s, 'e-(aq) H2 OH- H2O'.split(), '->', Reaction)
		assert rxn2.__class__ == Reaction
		assert rxn2.reac['e-(aq)'] == 2
		assert rxn2.inact_reac['H2O'] == 2
		assert rxn2.prod['H2'] == 1
		assert rxn2.prod['OH-'] == 2
		assert rxn2.param == 1e6
	
	r1 = to_reaction("-> H2O", None, '->', Reaction)
	assert r1.reac == {}
	assert r1.prod == {'H2O': 1}
	assert r1.param is None
	
	r2 = to_reaction("H2O ->", None, '->', Reaction)
	assert r2.reac == {'H2O': 1}
	assert r2.prod == {}
	assert r2.param is None
	
	rxn3 = to_reaction("H2O + H2O -> H3O+ + OH-", 'H3O+ OH- H2O'.split(), '->', Reaction)
	assert rxn3.reac == {'H2O': 2} and rxn3.prod == {'H3O+': 1, 'OH-': 1}
	
	rxn4 = to_reaction("2 e-(aq) + (2 H2O) + (2 H+) -> H2 + 2 H2O", 'e-(aq) H2 H2O H+'.split(), '->', Reaction)
	assert rxn4.reac == {'e-(aq)': 2} and rxn4.inact_reac == {'H2O': 2, 'H+': 2} and rxn4.prod == {'H2': 1, 'H2O': 2}


def test_Reaction_string():
	from sympy import S
	r = Reaction({'A': 1, 'B': 2}, {'C': S(3)/2}, checks=[
			chk for chk in Reaction.default_checks if chk != 'all_integral'])
	assert r.string() == 'A + 2 B -> 3/2 C'
	assert r.string(Reaction_arrow='-->', Reaction_coeff_space='') == 'A + 2B --> 3/2C'
