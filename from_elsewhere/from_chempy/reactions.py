#!/usr/bin/env python3
#
#  chemistry.py
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


import copy
import math
from collections import defaultdict, OrderedDict
from functools import reduce
from itertools import chain, product
from operator import add, mul

import quantities  # type: ignore
from mathematical.utils import intdiv  # type: ignore # TODO

from chemistry_tools.dicts import ArithmeticDict
from chemistry_tools.units import is_quantity, to_unitless, unit_of
from .parsing import (
	to_reaction,
	)




def _parse_multiplicity(strings: Iterable[str], substance_keys=None) -> Dict[str, float]:
	"""

	**Examples**
	>>> _parse_multiplicity(['2 H2O2', 'O2']) == {'H2O2': 2, 'O2': 1}
	True
	>>> _parse_multiplicity(['2 * H2O2', 'O2']) == {'H2O2': 2, 'O2': 1}
	True
	>>> _parse_multiplicity(['']) == {}
	True
	>>> _parse_multiplicity(['H2O', 'H2O']) == {'H2O': 2}
	True

	:param strings:
	:type strings:
	:param substance_keys:
	:type substance_keys:

	:return:
	"""

	result: Dict[str, float] = {}

	for items in [re.split(' \\* | ', s) for s in strings]:
		items = [x for x in items if x != '']

		if len(items) == 0:
			continue

		elif len(items) == 1:
			if items[0] not in result:
				result[items[0]] = 0

			result[items[0]] += 1

		elif len(items) == 2:
			if items[1] not in result:
				result[items[1]] = 0

			result[items[1]] += float(items[0]) if '.' in items[0] or 'e' in items[0] else int(items[0])

		else:
			raise ValueError("To many parts in substring")

	if substance_keys is not None:
		for k in result:
			if k not in substance_keys:
				raise ValueError(f"Unknown substance_key: {k}")

	return result



def to_reaction(line, substance_keys, token, cls, globals_=None, **kwargs):
	"""
	Parses a string into a Reaction object and substances

	Reac1 + 2 Reac2 + (2 Reac1) -> Prod1 + Prod2; 10**3.7; ref='doi:12/ab'
	Reac1 = Prod1; 2.1;

	Parameters
	----------
	line: str
		string representation to be parsed
	substance_keys: iterable of strings
		Allowed names, e.g. ('H2O', 'H+', 'OH-')
	token : str
		delimiter token between reactant and product side
	cls : class
		e.g. subclass of Reaction
	globals_: dict (optional)
		Globals passed on to :func:`eval`, when ``None``:
		`chempy.units` is used with 'chempy'
		and 'default_units' extra entries.

	Notes
	-----
	This function calls :func:`eval`, hence there are severe security concerns
	with running this on untrusted data.

	"""

	parts = line.rstrip('\n').split(';')
	stoich = parts[0].strip()
	if len(parts) > 2:
		kwargs.update(eval('dict(' + ';'.join(parts[2:]) + '\n)', globals_ or {}))
	if len(parts) > 1:
		param = parts[1].strip()
	else:
		param = kwargs.pop('param', 'None')

	if isinstance(param, str):
		param = None if globals_ is False else eval(param, globals_)

	if token not in stoich:
		raise ValueError("Missing token: %s" % token)

	reac_prod = [[y.strip() for y in x.split(' + ')] for x in stoich.split(token)]

	act, inact = [], []
	for elements in reac_prod:
		act.append(_parse_multiplicity([x for x in elements if not x.startswith('(')], substance_keys))
		inact.append(_parse_multiplicity(
				[x[1:-1] for x in elements if x.startswith('(') and x.endswith(')')],
				substance_keys
				))

	# stoich coeff -> dict
	return cls(act[0], act[1], param, inact_reac=inact[0], inact_prod=inact[1], **kwargs)




class Reaction:
	"""
	Class representing a chemical reaction

	Consider for example:

		2 R --> A + P; r = k*A*R*R

	this would be represented as ``Reaction({'A': 1, 'R': 2},
	{'A': 2, 'P': 1}, param=k)``. Some reactions have a larger
	stoichiometric coefficient than what appears in the rate
	expression, e.g.:

		5 A + B --> C; r = k*A*B

	this can be represented as ``Reaction({'C1': 1, 'C2': 1},
	{'B': 1}, inact_reac={'C1': 4}, param=k)``.

	The rate constant information in ``param`` may be a subclass of
	:class:`chempy.kinetics.rates.RateExpr` or carry a :meth:`as_RateExpr`,
	if neither: `param` will be assumed to be a rate constant for a mass-action
	type of kinetic expression.

	Additional data may be stored in the ``data`` dict.


	Parameters
	----------
	reac : dict (str -> int)
		If ``reac`` is a ``set``, then multiplicities are assumed to be 1.
	prod : dict (str -> int)
		If ``prod`` is a ``set``, then multiplicities are assumed to be 1.
	param : float or callable
		Special case (side-effect): if param is a subclass of
		:class:`.kinetics.rates.RateExpr` and its :attr:`rxn`
		is `None` it will be set to `self`.
	inact_reac : dict (optional)
	inact_prod : dict (optional)
	name : str (optional)
	k : deprecated (alias for param)
	ref : object
		Reference (e.g. a string containing doi number).
	data : dict (optional)
	checks : iterable of str
		Raises ``ValueError`` if any method ``check_%s`` returns False
		for all ``%s`` in ``checks``. Default: ``Reaction.default_checks``.

	Attributes
	----------
	reac : OrderedDict
	prod : OrderedDict
	param : object
	inact_reac : OrderedDict
	inact_prod : OrderedDict
	name : str
	ref : str
	data : dict

	**Examples**
	>>> r = Reaction({'H2': 2, 'O2': 1}, {'H2O': 2})
	>>> r.keys() == {'H2', 'O2', 'H2O'}
	True
	>>> r.order()
	3
	>>> r.net_stoich(['H2', 'H2O', 'O2'])
	(-2, 2, -1)
	>>> print(r)
	2 H2 + O2 -> 2 H2O

	"""
	
	_cmp_attr = ('reac', 'prod', 'param', 'inact_reac', 'inact_prod')
	_all_attr = _cmp_attr + ('name', 'ref', 'data')
	_str_arrow = '->'
	
	param_char = 'k'  # convention
	default_checks = {'any_effect', 'all_positive', 'all_integral', 'consistent_units'}
	
	@staticmethod
	def _init_stoich(container):
		if isinstance(container, set):
			container = {k: 1 for k in container}
		container = container or {}
		if type(container) == dict:  # we don't want isinstance here in case of OrderedDict
			container = OrderedDict(sorted(container.items(), key=lambda kv: kv[0]))
		return container
	
	def __init__(
			self, reac, prod, param=None, inact_reac=None, inact_prod=None,
			name=None, ref=None, data=None, checks=None, dont_check=None):
		self.reac = self._init_stoich(reac)
		self.inact_reac = self._init_stoich(inact_reac)
		self.prod = self._init_stoich(prod)
		self.inact_prod = self._init_stoich(inact_prod)
		self.param = param
		self.name = name
		self.ref = ref
		self.data = data or {}
		if checks is not None and dont_check is not None:
			raise ValueError("Cannot specify both checks and dont_check")
		if checks is None:
			checks = self.default_checks ^ (dont_check or set())
		
		for check in checks:
			getattr(self, 'check_' + check)(throw=True)
	
	@classmethod
	def from_string(cls, string, substance_keys=None, globals_=None, **kwargs):
		"""
		Parses a string into a Reaction instance

		Parameters
		----------
		string : str
			String representation of the reaction.
		substance_keys : convertible to iterable of strings or string or None
			Used prevent e.g. misspelling.
			if str: split is invoked, if None: no checking done.
		globals_ : dict (optional)
			Dictionary for eval for (default: None -> {'chempy': chempy})
			If ``False``: no eval will be called (useful for web-apps).
		**kwargs :
			Passed on to constructor.

		**Examples**
		>>> r = Reaction.from_string("H2O -> H+ + OH-; 1e-4", 'H2O H+ OH-')
		>>> r.reac == {'H2O': 1} and r.prod == {'H+': 1, 'OH-': 1}
		True
		>>> r2 = Reaction.from_string("2 H2O -> 2 H2 + O2", 'H2O H2 O2')
		>>> r2.reac == {'H2O': 2} and r2.prod == {'H2': 2, 'O2': 1}
		True
		>>> r3 = Reaction.from_string("A -> B; 1/second", 'A B')
		>>> from chemistry_tools.units import to_unitless, quantities
		>>> to_unitless(r3.param, quantities.hour**-1)
		3600.0
		>>> r4 = Reaction.from_string("A -> 2 B; 'k'", 'A B')
		>>> r4.rate(dict(A=3, B=5, k=7)) == {'A': -3*7, 'B': 2*3*7}
		True
		>>> r5 = Reaction.from_string("A -> B; 1/molar/second", 'A B')
		Traceback (most recent call last):
			...
		ValueError: Unable to convert between units ...


		Notes
		-----
		:func:`chempy.util.parsing.to_reaction` is used which in turn calls
		:func:`eval` which is a severe security concern for untrusted input.
		"""
		
		if isinstance(substance_keys, str):
			if ' ' in substance_keys:
				substance_keys = substance_keys.split()
		return to_reaction(string, substance_keys, cls._str_arrow, cls, globals_, **kwargs)
	
	def copy(self, **kwargs):
		if 'checks' not in kwargs:
			kwargs['checks'] = ()
		for k in self._all_attr:
			if k not in kwargs:
				kwargs[k] = copy.copy(getattr(self, k))
		return self.__class__(**kwargs)
	
	def check_any_effect(self, throw=False):
		"""
		Checks if the reaction has any effect
		"""
		
		if not any(self.net_stoich(self.keys())):
			if throw:
				raise ValueError("The net stoichiometry change of all species are zero.")
			else:
				return False
		return True
	
	def check_all_positive(self, throw=False):
		"""
		Checks if all stoichiometric coefficients are positive
		"""
		
		for nam, cont in [(nam, getattr(self, nam)) for nam in 'reac prod inact_reac inact_prod'.split()]:
			for k, v in cont.items():
				if v < 0:
					if throw:
						raise ValueError(f"Found a negative stoichiometry for {k} in {nam}.")
					else:
						return False
		return True
	
	def check_all_integral(self, throw=False):
		"""
		Checks if all stoichiometric coefficients are integers """
		for nam, cont in [(nam, getattr(self, nam)) for nam in 'reac prod inact_reac inact_prod'.split()]:
			for k, v in cont.items():
				if v != type(v)(int(v)):
					if throw:
						raise ValueError(f"Found a non-integer stoichiometric coefficient for {k} in {nam}.")
					else:
						return False
		return True
	
	def check_consistent_units(self, throw=False):
		if is_quantity(self.param):  # This will assume mass action
			try:
				to_unitless(self.param / (
						quantities.molar ** (1 - self.order()) / quantities.s))
			except:
				if throw:
					raise
				else:
					return False
			else:
				return True
		else:
			return True  # the user might not be using ``chemistry_tools.units``
	
	def __eq__(lhs, rhs):
		if lhs is rhs:
			return True
		if not isinstance(lhs, Reaction) or not isinstance(rhs, Reaction):
			return NotImplemented
		for attr in lhs._cmp_attr:
			if getattr(lhs, attr) != getattr(rhs, attr):
				return False
		return True
	
	def __hash__(self):
		return sum(map(hash, (getattr(self, k) for k in ['reac', 'prod', 'param', 'inact_reac', 'inact_prod'])))
	
	def order(self):
		"""
		Sum of (active) reactant stoichiometries """
		return sum(self.reac.values())
	
	def keys(self):
		return set(chain(
				self.reac.keys(), self.prod.keys(),
				self.inact_reac.keys(), self.inact_prod.keys()))
	
	def net_stoich(self, substance_keys):
		"""
		Per substance net stoichiometry tuple (active & inactive)
		"""
		
		return tuple(
				self.prod.get(k, 0) - self.reac.get(k, 0) +
				self.inact_prod.get(k, 0) - self.inact_reac.get(k, 0) for k in substance_keys)
	
	def all_reac_stoich(self, substances):
		"""
		Per substance reactant stoichiometry tuple (active & inactive)
		"""
		
		return tuple(self.reac.get(k, 0) + self.inact_reac.get(k, 0) for k in substances)
	
	def active_reac_stoich(self, substances):
		"""
		Per substance reactant stoichiometry tuple (active)
		"""
		
		return tuple(self.reac.get(k, 0) for k in substances)
	
	def all_prod_stoich(self, substances):
		"""
		Per substance product stoichiometry tuple (active & inactive)
		"""
		
		return tuple(self.prod.get(k, 0) + self.inact_prod.get(k, 0) for k in substances)
	
	def active_prod_stoich(self, substances):
		"""
		Per substance product stoichiometry tuple (active)
		"""
		
		return tuple(self.prod.get(k, 0) for k in substances)
	
	def _xprecipitate_stoich(self, substances, xor):
		return tuple((
						0 if xor ^ (getattr(v, 'phase_idx', 0) > 0)
						else self.prod.get(k, 0) + self.inact_prod.get(k, 0) -
							 self.reac.get(k, 0) - self.inact_reac.get(k, 0)
						) for k, v in substances.items())
	
	def precipitate_stoich(self, substances):
		"""
		Only stoichiometry of precipitates
		"""
		
		net = self._xprecipitate_stoich(substances, True)
		found1 = -1
		for idx in range(len(net)):
			if net[idx] != 0:
				if found1 == -1:
					found1 = idx
				else:
					raise NotImplementedError("Only one precipitate assumed.")
		return net, net[found1], found1
	
	def non_precipitate_stoich(self, substances):
		"""
		Only stoichiometry of non-precipitates
		"""
		
		return self._xprecipitate_stoich(substances, False)
	
	def has_precipitates(self, substances):
		for s_name in chain(self.reac.keys(), self.prod.keys(), self.inact_reac.keys(), self.inact_prod.keys()):
			if getattr(substances[s_name], 'phase_idx', 0) > 0:
				return True
		return False
	
	def string(self, substances=None, with_param=False, with_name=False, **kwargs):
		"""
		Returns a string representation of the reaction

		Parameters
		----------
		substances: dict
			mapping substance keys to Substance instances
		with_param: bool
			whether to print the parameter (default: False)
		with_name: bool
			whether to print the name (default: False)

		**Examples**
		>>> r = Reaction({'H+': 1, 'Cl-': 1}, {'HCl': 1}, 1e10)
		>>> r.string(with_param=False)
		'Cl- + H+ -> HCl'
		"""
		
		from .printing import str_
		return str_(self, substances=substances, with_param=with_param, with_name=with_name, **kwargs)
	
	def __str__(self) -> str:
		return self.string(with_param=True, with_name=True)
	
	def latex(self, substances, with_param=False, with_name=False, **kwargs):
		r"""
		Returns a LaTeX representation of the reaction

		Parameters
		----------
		substances: dict
			mapping substance keys to Substance instances
		with_param: bool
			whether to print the parameter (default: False)
		with_name: bool
			whether to print the name (default: False)

		**Examples**
		>>> keys = 'H2O H+ OH-'.split()
		>>> subst = {k: Substance.from_formula(k) for k in keys}
		>>> r = Reaction.from_string("H2O -> H+ + OH-; 1e-4", subst)
		>>> r.latex(subst) == r'H_{2}O \rightarrow H^{+} + OH^{-}'
		True
		>>> r2 = Reaction.from_string("H+ + OH- -> H2O; 1e8/molar/second", subst)
		>>> ref = r'H^{+} + OH^{-} \rightarrow H_{2}O; 10^{8} $\mathrm{\frac{1}{(s{\cdot}M)}}$'
		>>> r2.latex(subst, with_param=True) == ref
		True
		"""
		
		from .printing import latex
		return latex(self, substances=substances, with_param=with_param, with_name=with_name, **kwargs)
	
	def unicode(self, substances, with_param=False, with_name=False, **kwargs):
		"""
		Returns a unicode string representation of the reaction

		**Examples**
		>>> keys = 'H2O H+ OH-'.split()
		>>> subst = {k: Substance.from_formula(k) for k in keys}
		>>> r = Reaction.from_string("H2O -> H+ + OH-; 1e-4", subst)
		>>> r.unicode(subst) == u'H₂O → H⁺ + OH⁻'
		True
		>>> r2 = Reaction.from_string("H+ + OH- -> H2O; 1e8/molar/second", subst)
		>>> r2.unicode(subst, with_param=True) == u'H⁺ + OH⁻ → H₂O; 10⁸ 1/(s·M)'
		True
		"""
		
		from .printing import unicode_
		return unicode_(self, substances=substances, with_param=with_param,
						with_name=with_name, **kwargs)
	
	def html(self, substances, with_param=False, with_name=False, **kwargs):
		""" Returns a HTML representation of the reaction

		**Examples**
		>>> keys = 'H2O H+ OH-'.split()
		>>> subst = {k: Substance.from_formula(k) for k in keys}
		>>> r = Reaction.from_string("H2O -> H+ + OH-; 1e-4", subst)
		>>> r.html(subst)
		'H<sub>2</sub>O &rarr; H<sup>+</sup> + OH<sup>-</sup>'
		>>> r2 = Reaction.from_string("H+ + OH- -> H2O; 1e8/molar/second", subst)
		>>> r2.html(subst, with_param=True)
		'H<sup>+</sup> + OH<sup>-</sup> &rarr; H<sub>2</sub>O&#59; 10<sup>8</sup> 1/(s*M)'

		"""
		from .printing import html
		return html(self, with_param=with_param, with_name=with_name,
					substances=substances, **kwargs)
	
	def _repr_html_(self):
		return self.html({k: k for k in self.keys()})
	
	def _violation(self, substances, attr):
		net = 0.0
		for substance, coeff in zip(substances.values(),
									self.net_stoich(substances.keys())):
			net += getattr(substance, attr) * coeff
		return net
	
	def mass_balance_violation(self, substances):
		"""
		Net amount of mass produced

		Parameters
		----------
		substances: dict

		Returns
		-------
		float: amount of net mass produced/consumed
		"""
		
		return self._violation(substances, 'mass')
	
	def charge_neutrality_violation(self, substances):
		"""
		Net amount of charge produced

		Parameters
		----------
		substances: dict

		Returns
		-------
		float: amount of net charge produced/consumed
		"""
		
		return self._violation(substances, 'charge')
	
	def composition_violation(self, substances, composition_keys=None):
		"""
		Net amount of constituent produced

		If composition keys correspond to conserved entities e.g. atoms
		in chemical reactions, this function should return a list of zeros.

		Parameters
		----------
		substances : dict
		composition_keys : iterable of str, ``None`` or ``True``
			When ``None`` or True: composition keys are taken from substances.
			When ``True`` the keys are also return as an extra return value

		Returns
		-------
		- If ``composition_keys == True``: a tuple: (violations, composition_keys)
		- Otherwise: violations (list of coefficients)
		"""
		
		keys, values = zip(*substances.items())
		ret_comp_keys = composition_keys is True
		if composition_keys in (None, True):
			composition_keys = Substance.composition_keys(values)
		net = [0] * len(composition_keys)
		for substance, coeff in zip(values, self.net_stoich(keys)):
			for idx, key in enumerate(composition_keys):
				net[idx] += substance.composition.get(key, 0) * coeff
		if ret_comp_keys:
			return net, composition_keys
		else:
			return net


def equilibrium_quotient(concs, stoich):
	"""
	Calculates the equilibrium quotient of an equilbrium

	Parameters
	----------
	concs: array_like
		per substance concentration
	stoich: iterable of integers
		per substance stoichiometric coefficient

	**Examples**
	>>> '%.12g' % equilibrium_quotient([1.0, 1e-7, 1e-7], [-1, 1, 1])
	'1e-14'

	"""
	
	import numpy  # type: ignore
	
	if not hasattr(concs, 'ndim') or concs.ndim == 1:
		tot = 1
	else:
		tot = numpy.ones(concs.shape[0])
		concs = concs.T
	
	for nr, conc in zip(stoich, concs):
		tot *= conc ** nr
	return tot


class Equilibrium(Reaction):
	"""
		Represents an equilibrium reaction

	See :class:`Reaction` for parameters

	"""
	_str_arrow = '='
	param_char = 'K'  # convention
	
	def check_consistent_units(self, throw=False):
		if is_quantity(self.param):  # This will assume mass action
			exponent = sum(self.prod.values()) - sum(self.reac.values())
			unit_param = unit_of(self.param, simplified=True)
			unit_expected = unit_of(quantities.molar ** exponent, simplified=True)
			if unit_param == unit_expected:
				return True
			else:
				if throw:
					raise ValueError("Inconsistent units in equilibrium: %s vs %s" %
									 (unit_param, unit_expected))
				else:
					return False
		else:
			return True  # the user might not be using ``chemistry_tools.units``
	
	def as_reactions(self, kf=None, kb=None, units=None, variables=None, backend=math, new_name=None, **kwargs):
		"""
		Creates a forward and backward :class:`Reaction` pair

		Parameters
		----------
		kf : float or RateExpr
		kb : float or RateExpr
		units : module
		variables : dict, optional
		backend : module

		"""
		nb = sum(self.prod.values())
		nf = sum(self.reac.values())
		if units is None:
			if hasattr(kf, 'units') or hasattr(kb, 'units'):
				raise ValueError("units missing")
			c0 = 1
		else:
			c0 = 1 * units.molar  # standard concentration IUPAC
		
		if kf is None:
			fw_name = self.name
			bw_name = new_name
			if kb is None:
				try:
					kf, kb = self.param
				except TypeError:
					raise ValueError("Exactly one rate needs to be provided")
			else:
				kf = kb * self.param * c0 ** (nb - nf)
		elif kb is None:
			kb = kf / (self.param * c0 ** (nb - nf))
			fw_name = new_name
			bw_name = self.name
		else:
			raise ValueError("Exactly one rate needs to be provided")
		
		return (
				Reaction(self.reac, self.prod, kf, self.inact_reac,
						 self.inact_prod, ref=self.ref, name=fw_name, **kwargs),
				Reaction(self.prod, self.reac, kb, self.inact_prod,
						 self.inact_reac, ref=self.ref, name=bw_name, **kwargs)
				)
	
	def equilibrium_expr(self):
		"""
		Turns self.param into a :class:`EqExpr` instance (if not already)

		**Examples**
		>>> r = Equilibrium.from_string('2 A + B = 3 C; 7')
		>>> eqex = r.equilibrium_expr()
		>>> eqex.args[0] == 7
		True

		"""
		from .util._expr import Expr
		from .thermodynamics import MassActionEq
		if isinstance(self.param, Expr):
			return self.param
		else:
			try:
				convertible = self.param.as_EqExpr
			except AttributeError:
				return MassActionEq([self.param])
			else:
				return convertible()
	
	def equilibrium_constant(self, variables=None, backend=math):
		"""
		Return equilibrium constant

		Parameters
		----------
		variables : dict, optional
		backend : module, optional

		"""
		return self.equilibrium_expr().eq_const(variables, backend=backend)
	
	def equilibrium_equation(self, variables, backend=None, **kwargs):
		return self.equilibrium_expr().equilibrium_equation(
				variables, equilibrium=self, backend=backend, **kwargs)
	
	def Q(self, substances, concs):
		"""
		Calculates the equilibrium qoutient """
		stoich = self.non_precipitate_stoich(substances)
		return equilibrium_quotient(concs, stoich)
	
	def precipitate_factor(self, substances, sc_concs):
		factor = 1
		for r, n in self.reac.items():
			if r.precipitate:
				factor *= sc_concs[substances.index(r)] ** -n
		for p, n in self.prod.items():
			if p.precipitate:
				factor *= sc_concs[substances.index(p)] ** n
		return factor
	
	def dimensionality(self, substances):
		result = 0
		for r, n in self.reac.items():
			if getattr(substances[r], 'phase_idx', 0) > 0:
				continue
			result -= n
		for p, n in self.prod.items():
			if getattr(substances[p], 'phase_idx', 0) > 0:
				continue
			result += n
		return result
	
	def __rmul__(self, other):  # This works on both Py2 and Py3
		try:
			other_is_int = other.is_integer
		except AttributeError:
			other_is_int = isinstance(other, int)
		if not other_is_int or not isinstance(self, Equilibrium):
			return NotImplemented
		param = None if self.param is None else self.param ** other
		if other < 0:
			other *= -1
			flip = True
		else:
			flip = False
		other = int(other)  # convert SymPy "Integer" to Pyton "int"
		reac = dict(other * ArithmeticDict(int, self.reac))
		prod = dict(other * ArithmeticDict(int, self.prod))
		inact_reac = dict(other * ArithmeticDict(int, self.inact_reac))
		inact_prod = dict(other * ArithmeticDict(int, self.inact_prod))
		if flip:
			reac, prod = prod, reac
			inact_reac, inact_prod = inact_prod, inact_reac
		return Equilibrium(reac, prod, param,
						   inact_reac=inact_reac, inact_prod=inact_prod)
	
	def __neg__(self):
		return -1 * self
	
	def __mul__(self, other):
		return other * self
	
	def __add__(self, other):
		keys = set()
		for key in chain(self.reac.keys(), self.prod.keys(),
						 other.reac.keys(), other.prod.keys()):
			keys.add(key)
		reac, prod = {}, {}
		for key in keys:
			n = (self.prod.get(key, 0) - self.reac.get(key, 0) +
				 other.prod.get(key, 0) - other.reac.get(key, 0))
			if n < 0:
				reac[key] = -n
			elif n > 0:
				prod[key] = n
			else:
				pass  # n == 0
		if (self.param, other.param) == (None, None):
			param = None
		else:
			param = self.param * other.param
		return Equilibrium(reac, prod, param)
	
	def __sub__(self, other):
		return self + -1 * other
	
	@staticmethod
	def eliminate(rxns, wrt):
		"""
		Linear combination coefficients for elimination of a substance

		Parameters
		----------
		rxns : iterable of Equilibrium instances
		wrt : str (substance key)

		**Examples**
		>>> e1 = Equilibrium({'Cd+2': 4, 'H2O': 4}, {'Cd4(OH)4+4': 1, 'H+': 4}, 10**-32.5)
		>>> e2 = Equilibrium({'Cd(OH)2(s)': 1}, {'Cd+2': 1, 'OH-': 2}, 10**-14.4)
		>>> Equilibrium.eliminate([e1, e2], 'Cd+2')
		[1, 4]
		>>> print(1*e1 + 4*e2)
		4 Cd(OH)2(s) + 4 H2O = Cd4(OH)4+4 + 4 H+ + 8 OH-; 7.94e-91

		"""
		import sympy
		viol = [r.net_stoich([wrt])[0] for r in rxns]
		factors = defaultdict(int)
		for v in viol:
			for f in sympy.primefactors(v):
				factors[f] = max(factors[f], sympy.Abs(v // f))
		rcd = reduce(mul, (k ** v for k, v in factors.items()))
		viol[0] *= -1
		return [rcd // v for v in viol]
	
	def cancel(self, rxn):
		"""
		Multiplier of how many times rxn can be added/subtracted.

		Parameters
		----------
		rxn : Equilibrium

		**Examples**
		>>> e1 = Equilibrium({'Cd(OH)2(s)': 4, 'H2O': 4},
		...                  {'Cd4(OH)4+4': 1, 'H+': 4, 'OH-': 8}, 7.94e-91)
		>>> e2 = Equilibrium({'H2O': 1}, {'H+': 1, 'OH-': 1}, 10**-14)
		>>> e1.cancel(e2)
		-4
		>>> print(e1 - 4*e2)
		4 Cd(OH)2(s) = Cd4(OH)4+4 + 4 OH-; 7.94e-35

		"""
		keys = rxn.keys()
		s1 = self.net_stoich(keys)
		s2 = rxn.net_stoich(keys)
		candidate = float('inf')
		for v1, v2 in zip(s1, s2):
			r = intdiv(-v1, v2)
			candidate = min(candidate, r, key=abs)
		return candidate


def _solve_balancing_ilp_pulp(A):
	import pulp
	x = [pulp.LpVariable('x%d' % i, lowBound=1, cat='Integer') for i in range(A.shape[1])]
	prob = pulp.LpProblem("chempy balancing problem", pulp.LpMinimize)
	prob += reduce(add, x)
	for expr in [pulp.lpSum([x[i] * e for i, e in enumerate(row)]) for row in A.tolist()]:
		prob += expr == 0
	prob.solve()
	return [pulp.value(_) for _ in x]


def balance_stoichiometry(reactants, products, substances=None,
						  substance_factory=Substance.from_formula,
						  parametric_symbols=None, underdetermined=True, allow_duplicates=False):
	"""
		Balances stoichiometric coefficients of a reaction

	Parameters
	----------
	reactants : iterable of reactant keys
	products : iterable of product keys
	substances : OrderedDict or string or None
		Mapping reactant/product keys to instances of :class:`Substance`.
	substance_factory : callback
	parametric_symbols : generator of symbols
		Used to generate symbols for parametric solution for
		under-determined system of equations. Default is numbered "x-symbols" starting
		from 1.
	underdetermined : bool
		Allows to find a non-unique solution (in addition to a constant factor
		across all terms). Set to ``False`` to disallow (raise ValueError) on
		e.g. "C + O2 -> CO + CO2". Set to ``None`` if you want the symbols replaced
		so that the coefficients are the smallest possible positive (non-zero) integers.
	allow_duplicates : bool
		If False: raises an excpetion if keys appear in both ``reactants`` and ``products``.

	**Examples**
	>>> ref = {'C2H2': 2, 'O2': 3}, {'CO': 4, 'H2O': 2}
	>>> balance_stoichiometry({'C2H2', 'O2'}, {'CO', 'H2O'}) == ref
	True
	>>> ref2 = {'H2': 1, 'O2': 1}, {'H2O2': 1}
	>>> balance_stoichiometry('H2 O2'.split(), ['H2O2'], 'H2 O2 H2O2') == ref2
	True
	>>> reac, prod = 'CuSCN KIO3 HCl'.split(), 'CuSO4 KCl HCN ICl H2O'.split()
	>>> Reaction(*balance_stoichiometry(reac, prod)).string()
	'4 CuSCN + 7 KIO3 + 14 HCl -> 4 CuSO4 + 7 KCl + 4 HCN + 7 ICl + 5 H2O'
	>>> balance_stoichiometry({'Fe', 'O2'}, {'FeO', 'Fe2O3'}, underdetermined=False)
	Traceback (most recent call last):
		...
	ValueError: The system was under-determined
	>>> r, p = balance_stoichiometry({'Fe', 'O2'}, {'FeO', 'Fe2O3'})
	>>> list(set.union(*[v.free_symbols for v in r.values()]))
	[x1]
	>>> b = balance_stoichiometry({'Fe', 'O2'}, {'FeO', 'Fe2O3'}, underdetermined=None)
	>>> b == ({'Fe': 3, 'O2': 2}, {'FeO': 1, 'Fe2O3': 1})
	True
	>>> d = balance_stoichiometry({'C', 'CO'}, {'C', 'CO', 'CO2'}, underdetermined=None, allow_duplicates=True)
	>>> d == ({'CO': 2}, {'C': 1, 'CO2': 1})
	True

	Returns
	-------
	balanced reactants : dict
	balanced products : dict

	"""
	import sympy
	from sympy import (
		MutableDenseMatrix, gcd, zeros, linsolve, numbered_symbols, Wild, Symbol,
		Integer, Tuple, preorder_traversal as pre,
		)
	
	_intersect = sorted(set.intersection(*map(set, (reactants, products))))
	if _intersect:
		if allow_duplicates:
			if underdetermined is not None:
				raise NotImplementedError("allow_duplicates currently requires underdetermined=None")
			if set(reactants) == set(products):
				raise ValueError("cannot balance: reactants and products identical")
			
			# For each duplicate, try to drop it completely:
			for dupl in _intersect:
				try:
					result = balance_stoichiometry(
							[sp for sp in reactants if sp != dupl],
							[sp for sp in products if sp != dupl],
							substances=substances, substance_factory=substance_factory,
							underdetermined=underdetermined, allow_duplicates=True)
				except Exception:
					continue
				else:
					return result
			for perm in product(*[(False, True)] * len(_intersect)):  # brute force (naive)
				r = set(reactants)
				p = set(products)
				for remove_reac, dupl in zip(perm, _intersect):
					if remove_reac:
						r.remove(dupl)
					else:
						p.remove(dupl)
				try:
					result = balance_stoichiometry(
							r, p, substances=substances, substance_factory=substance_factory,
							parametric_symbols=parametric_symbols, underdetermined=underdetermined,
							allow_duplicates=False)
				except ValueError:
					continue
				else:
					return result
			else:
				raise ValueError("Failed to remove duplicate keys: %s" % _intersect)
		else:
			raise ValueError("Substances on both sides: %s" % str(_intersect))
	if substances is None:
		substances = OrderedDict([(k, substance_factory(k)) for k in chain(reactants, products)])
	if isinstance(substances, str):
		substances = OrderedDict([(k, substance_factory(k)) for k in substances.split()])
	if type(reactants) == set:  # we don't want isinstance since it might be "OrderedSet"
		reactants = sorted(reactants)
	if type(products) == set:
		products = sorted(products)
	subst_keys = list(reactants) + list(products)
	
	cks = Substance.composition_keys(substances.values())
	
	if parametric_symbols is None:
		parametric_symbols = numbered_symbols('x', start=1, integer=True, positive=True)
	
	# ?C2H2 + ?O2 -> ?CO + ?H2O
	# Ax = 0
	#   A:                    x:
	#
	#   C2H2   O2  CO  H2O
	# C -2     0    1   0      x0    =   0
	# H -2     0    0   2      x1        0
	# O  0    -2    1   1      x2        0
	#                          x3
	
	def _get(ck, sk):
		return substances[sk].composition.get(ck, 0) * (-1 if sk in reactants else 1)
	
	for ck in cks:  # check that all components are present on reactant & product sides
		for rk in reactants:
			if substances[rk].composition.get(ck, 0) != 0:
				break
		else:
			any_pos = any(substances[pk].composition.get(ck, 0) > 0 for pk in products)
			any_neg = any(substances[pk].composition.get(ck, 0) < 0 for pk in products)
			if any_pos and any_neg:
				pass  # negative and positive parts among products, no worries
			else:
				raise ValueError("Component '%s' not among reactants" % ck)
		
		for pk in products:
			if substances[pk].composition.get(ck, 0) != 0:
				break
		else:
			any_pos = any(substances[pk].composition.get(ck, 0) > 0 for pk in reactants)
			any_neg = any(substances[pk].composition.get(ck, 0) < 0 for pk in reactants)
			if any_pos and any_neg:
				pass  # negative and positive parts among reactants, no worries
			else:
				raise ValueError("Component '%s' not among products" % ck)
	
	A = MutableDenseMatrix([[_get(ck, sk) for sk in subst_keys] for ck in cks])
	symbs = list(reversed([next(parametric_symbols) for _ in range(len(subst_keys))]))
	sol, = linsolve((A, zeros(len(cks), 1)), symbs)
	wi = Wild('wi', properties=[lambda k: not k.has(Symbol)])
	cd = reduce(gcd, [1] + [1 / m[wi] for m in map(
			lambda n: n.match(symbs[-1] / wi), pre(sol)) if m is not None])
	sol = sol.func(*[arg / cd for arg in sol.args])
	
	def remove(cont, symb, remaining):
		subsd = dict(zip(remaining / symb, remaining))
		cont = cont.func(*[(arg / symb).expand().subs(subsd) for arg in cont.args])
		if cont.has(symb):
			raise ValueError("Bug, please report an issue at https://github.com/bjodah/chempy")
		return cont
	
	done = False
	for idx, symb in enumerate(symbs):
		for expr in sol:
			iterable = expr.args if expr.is_Add else [expr]
			for term in iterable:
				if term.is_number:
					done = True
					break
			if done:
				break
		if done:
			break
		for expr in sol:
			if (expr / symb).is_number:
				sol = remove(sol, symb, MutableDenseMatrix(symbs[idx + 1:]))
				break
	for symb in symbs:
		cd = 1
		for expr in sol:
			iterable = expr.args if expr.is_Add else [expr]
			for term in iterable:
				if term.is_Mul and term.args[0].is_number and term.args[1] == symb:
					cd = gcd(cd, term.args[0])
		if cd != 1:
			sol = sol.func(*[arg.subs(symb, symb / cd) for arg in sol.args])
	
	if underdetermined == 1:
		underdetermined = None
	
	if underdetermined is None:
		sol = Tuple(*[Integer(x) for x in _solve_balancing_ilp_pulp(A)])
	
	fact = gcd(sol)
	sol = MutableDenseMatrix([e / fact for e in sol]).reshape(len(sol), 1)
	sol /= reduce(gcd, sol)
	if 0 in sol:
		raise ValueError("Superfluous species given.")
	if underdetermined:
		if any(x == sympy.nan for x in sol):
			raise ValueError("Failed to balance reaction")
	else:
		for x in sol:
			if len(x.free_symbols) != 0:
				raise ValueError("The system was under-determined")
		if not all(residual == 0 for residual in A * sol):
			raise ValueError("Failed to balance reaction")
	
	def _x(k):
		coeff = sol[subst_keys.index(k)]
		return int(coeff) if underdetermined is None else coeff
	
	return (
			OrderedDict([(k, _x(k)) for k in reactants]),
			OrderedDict([(k, _x(k)) for k in products])
			)


def mass_fractions(stoichiometries, substances=None, substance_factory=Substance.from_formula):
	"""
	Calculates weight fractions of each substance in a stoichiometric dict

	Parameters
	----------
	stoichiometries : dict or set
		If a ``set``: all entries are assumed to correspond to unit multiplicity.
	substances: dict or None

	**Examples**
	>>> r = mass_fractions({'H2': 1, 'O2': 1})
	>>> mH2, mO2 = 1.008*2, 15.999*2
	>>> abs(r['H2'] - mH2/(mH2+mO2)) < 1e-4
	True
	>>> abs(r['O2'] - mO2/(mH2+mO2)) < 1e-4
	True
	>>> mass_fractions({'H2O2'}) == {'H2O2': 1.0}
	True

	"""
	if isinstance(stoichiometries, set):
		stoichiometries = {k: 1 for k in stoichiometries}
	if substances is None:
		substances = OrderedDict([(k, substance_factory(k)) for k in stoichiometries])
	tot_mass = sum([substances[k].mass * v for k, v in stoichiometries.items()])
	return {k: substances[k].mass * v / tot_mass for k, v in stoichiometries.items()}
