#!/usr/bin/env python3
#
#  printer.py
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


# stdlib
import sys
from collections import OrderedDict
from itertools import chain
from math import floor, log10
from operator import itemgetter

from domdf_python_tools.doctools import append_docstring_from

# this package
from chemistry_tools.units import (
	_latex_from_dimensionality, html_of_unit, latex_of_unit, to_unitless, unicode_of_unit,
	unit_of,
	)
from chempy.parsing import _unicode_sup
from .chemistry import Substance


def number_to_scientific_html(number, uncertainty=None, unit=None, fmt=None):
	"""
	Formats a number as HTML (optionally with unit/uncertainty)

	Parameters
	----------
	number : float (w or w/o unit)
	uncertainty : same as number
	unit : unit
	fmt : int or callable

	Examples
	--------
	>>> number_to_scientific_html(3.14) == '3.14'
	True
	>>> number_to_scientific_html(3.14159265e-7)
	'3.1416&sdot;10<sup>-7</sup>'
	>>> number_to_scientific_html(1e13)
	'10<sup>13</sup>'
	>>> import quantities as pq
	>>> number_to_scientific_html(2**0.5 * pq.m / pq.s)
	'1.4142 m/s'
	"""
	
	return _number_to_X(number, uncertainty, unit, fmt, html_of_unit, _html_pow_10)


class Printer:
	_str = str
	_default_settings = dict(
			with_param=True,
			with_name=True,
			fallback_print_fn=str,
			Reaction_param_separator='; ',
			Reaction_coeff_space=' ',
			Reaction_around_arrow=(' ', ' '),
			magnitude_fmt=lambda x: '%.3g' % x,
			)
	_default_setting_factories = dict(
			substances=dict,
			colors=dict,  # substance key -> (bg-color, border-color), 6 char hex colors
			)
	_default_setting_attrs = dict(
			Reaction_coeff_fmt='_str',
			Reaction_formula_fmt='_str',
			unit_fmt='_str',
			)
	printmethod_attr = None  # e.g. '_html' or '_unicode', allows object local printing logic
	
	def __init__(self, settings=None):
		self._settings = dict(self._default_settings, **(settings or {}))
		for k, v in self._default_setting_factories.items():
			if k not in self._settings:
				self._settings[k] = v()
		for k, v in self._default_setting_attrs.items():
			if k not in self._settings:
				self._settings[k] = getattr(self, v)
		for k in self._settings:
			if k not in chain(self._default_settings, self._default_setting_factories,
							  self._default_setting_attrs):
				raise ValueError("Unknown setting: %s (missing in default_settings)" % k)
	
	def _get(self, key, **kwargs):
		return kwargs.get(key, self._settings[key])
	
	def _print(self, obj, **kwargs):
		for cls in type(obj).__mro__:
			print_meth = '_print_' + cls.__name__
			if hasattr(self, print_meth):
				return getattr(self, print_meth)(obj, **kwargs)
			for PrintCls in self.__class__.__mro__:
				_attr = getattr(PrintCls, 'printmethod_attr', None)
				if _attr and hasattr(obj, _attr):
					return getattr(obj, _attr)(self, **kwargs)
		fn = self._get('fallback_print_fn', **kwargs)
		if fn:
			return fn(obj)
		else:
			raise ValueError("Don't know how to print obj of type: %s" % type(obj))
	
	def doprint(self, obj):
		return self._print(obj)


class StrPrinter(Printer):
	_default_settings = dict(
		Printer._default_settings,
		repr_name='string',
		Equilibrium_arrow='=',
		Reaction_arrow='->',
		)

	def _reaction_parts(self, rxn, **kwargs):
		str_ = self._str
		coeff_fmt = self._get('Reaction_coeff_fmt', **kwargs)
		formula_fmt = self._get('Reaction_formula_fmt', **kwargs)
		substances = self._get('substances', **kwargs) or {}
		nullstr, space = str_(''), str_(self._get('Reaction_coeff_space'))
		reac, prod, i_reac, i_prod = [[
			(
				((coeff_fmt(v)+space) if v != 1 else nullstr) +
				formula_fmt(self._print(substances.get(k, k)))
				) for k, v in filter(itemgetter(1), d.items())
			] for d in (rxn.reac, rxn.prod, rxn.inact_reac, rxn.inact_prod)]
		r_str = str_(" + ").join(reac)
		ir_str = (str_(' + ( ') + str_(" + ").join(i_reac) + str_(')') if len(i_reac) > 0 else nullstr)
		arrow_str = self._get('%s_arrow' % rxn.__class__.__name__, **kwargs)
		p_str = str_(" + ").join(prod)
		ip_str = (str_(' + ( ') + str_(" + ").join(i_prod) + str_(')') if len(i_prod) > 0 else nullstr)
		return r_str, ir_str, arrow_str, p_str, ip_str

	def _reaction_str(self, rxn, **kwargs):
		fmtstr = self._str("{}{}%s{}%s{}{}") % self._get('Reaction_around_arrow', **kwargs)
		return fmtstr.format(*self._reaction_parts(rxn, **kwargs))

	def _reaction_param_str(self, rxn, **kwargs):
		mag_fmt = self._get('magnitude_fmt', **kwargs)
		unit_fmt = self._get('unit_fmt', **kwargs)
		try:
			magnitude_str = mag_fmt(rxn.param.magnitude)
			unit_str = unit_fmt(rxn.param.dimensionality)
		except AttributeError:
			try:
				return mag_fmt(rxn.param)
			except TypeError:
				return str(rxn.param)
		else:
			return magnitude_str + self._str(' ') + unit_str

	def _print_Reaction(self, rxn, **kwargs):
		res = self._reaction_str(rxn, **kwargs)
		if self._get('with_param', **kwargs) and rxn.param is not None:
			res += self._get('Reaction_param_separator', **kwargs)
			try:
				res += getattr(rxn.param, self._get('repr_name', **kwargs))(
					self._get('magnitude_fmt', **kwargs))
			except AttributeError:
				res += self._reaction_param_str(rxn, **kwargs)
		if self._get('with_name', **kwargs) and rxn.name is not None:
			res += self._get('Reaction_param_separator', **kwargs)
			res += rxn.name
		return res

	def _print_ReactionSystem(self, rsys, **kwargs):
		header = (rsys.name + '\n') if rsys.name else ''
		return header + '\n'.join(map(self._print, rsys.rxns)) + '\n'


def str_(obj, **settings):  # Python keyword, hence the trailing '_'
	return StrPrinter(settings).doprint(obj)


def number_to_scientific_unicode(number, uncertainty=None, unit=None, fmt=None):
	"""
	Formats a number as unicode (optionally with unit/uncertainty)

	Parameters
	----------
	number : float (w or w/o unit)
	uncertainty : same as number
	unit : unit
	fmt : int or callable

	Examples
	--------
	>>> number_to_scientific_unicode(3.14) == u'3.14'
	True
	>>> number_to_scientific_unicode(3.14159265e-7) == u'3.1416·10⁻⁷'
	True
	>>> import quantities as pq
	>>> number_to_scientific_unicode(2**0.5 * pq.m / pq.s)
	'1.4142 m/s'
	"""
	
	return _number_to_X(number, uncertainty, unit, fmt, unicode_of_unit, _unicode_pow_10)


class UnicodePrinter(StrPrinter):
	_default_settings = dict(
			StrPrinter._default_settings,
			repr_name='unicode',
			Equilibrium_arrow='⇌',
			Reaction_arrow='→',
			magnitude_fmt=number_to_scientific_unicode,
			unit_fmt=lambda dim: (
					dim.unicode if sys.version_info[0] > 2
					else dim.unicode.decode(encoding='utf-8')
			)
			)
	
	_str = str if sys.version_info[0] > 2 else unicode  # noqa
	
	def _print_Substance(self, s, **kwargs):
		return s.unicode_name or s.name


def unicode_(obj, **settings):  # Python 2 keyword, hence the trailing '_'
	return UnicodePrinter(settings).doprint(obj)


def _html_clsname(key):
	return "chempy_" + key.replace(
			'+', 'plus').replace(
			'-', 'minus').replace(
			'(', 'leftparen').replace(
			')', 'rightparen')


_html_semicolon = '&#59; '


class HTMLPrinter(StrPrinter):
	printmethod_attr = '_html'
	_default_settings = dict(
			StrPrinter._default_settings,
			repr_name='html',
			Equilibrium_arrow='&harr;',
			Reaction_arrow='&rarr;',
			Reaction_param_separator=_html_semicolon,
			magnitude_fmt=number_to_scientific_html
			)
	
	def _print_Substance(self, s, **kwargs):
		return s.html_name or s.name
	
	def _print_ReactionSystem(self, rsys, **kwargs):
		return super()._print_ReactionSystem(rsys, **kwargs).replace('\n', '<br>\n')


def html(obj, **settings):
	return HTMLPrinter(settings).doprint(obj)


class CSSPrinter(HTMLPrinter):
	def _print_Substance(self, s, **kwargs):
		key = s.name
		name = s.html_name or key
		common_sty = 'border-radius: 5pt; padding: 0pt 3pt 0pt 3pt;'
		colors = self._get('colors', **kwargs)
		if key in colors:
			style = f'background-color:#{colors[key] + (common_sty,)}; ' \
					f'border: 1px solid #{colors[key] + (common_sty,)}; ' \
					f'{colors[key] + (common_sty,)}'
		else:
			style = common_sty
		fmt = '<span class="%s" style="%s">%s</span>'
		return fmt % (_html_clsname(key), style, name)
	
	def _tr_id(self, rsys, i):
		return f'chempy_{id(rsys):d}_{i:d}'
	
	def _print_ReactionSystem(self, rsys, **kwargs):
		sep = '</td><td style="text-align:left;">&nbsp;'
		around = '</td><td style="text-align:center;">', '</td><td style="text-align:left;">'
		# cf. https://github.com/jupyter/notebook/issues/2160#issuecomment-352216152
		row_template = '<tr class="%s"><td style="text-align:right;">%s</td></tr>'
		rows = [row_template % (self._tr_id(rsys, i), s) for i, s in enumerate(map(
				lambda r: self._print(r, Reaction_param_separator=sep, Reaction_around_arrow=around),
				rsys.rxns
				))]
		tab_template = '<table class="chempy_ReactionSystem chempy_%d">%s%s</table>'
		header = '<tr><th style="text-align:center;" colspan="5">%s</th></tr>' % (rsys.name or '')
		return tab_template % (id(rsys), header, '\n\n'.join(rows))


def css(obj, **settings):
	return CSSPrinter(settings).doprint(obj)


def number_to_scientific_latex(number, uncertainty=None, unit=None, fmt=None):
	r"""
	Formats a number as LaTeX (optionally with unit/uncertainty)

	Parameters
	----------
	number : float (w or w/o unit)
	uncertainty : same as number
	unit : unit
	fmt : int or callable

	Examples
	--------
	>>> number_to_scientific_latex(3.14) == '3.14'
	True
	>>> number_to_scientific_latex(3.14159265e-7)
	'3.1416\\cdot 10^{-7}'
	>>> import quantities as pq
	>>> number_to_scientific_latex(2**0.5 * pq.m / pq.s)
	'1.4142\\,\\mathrm{\\frac{m}{s}}'
	>>> number_to_scientific_latex(1.23456, .789, fmt=2)
	'1.23(79)'
	"""
	
	return _number_to_X(number, uncertainty, unit, fmt, latex_of_unit, _latex_pow_10, r'\,')


class LatexPrinter(StrPrinter):
	_default_settings = dict(
			StrPrinter._default_settings,
			repr_name='latex',
			Equilibrium_arrow=r'\rightleftharpoons',
			Reaction_arrow=r'\rightarrow',
			magnitude_fmt=number_to_scientific_latex,
			unit_fmt=_latex_from_dimensionality
			)
	
	def _print_Substance(self, substance, **kwargs):
		return substance.latex_name or substance.name


def latex(obj, **settings):
	return LatexPrinter(settings).doprint(obj)



class Table:
	def __init__(self, rows, headers=None):
		self.rows, self.headers = rows, headers
	
	def _html(self, printer, **kwargs):
		def map_fmt(cont, fmt, joiner='\n'):
			return joiner.join(map(lambda x: fmt % printer._print(x, **kwargs), cont))
		
		rows = (
				[map_fmt(self.headers, '<th>%s</th>')] +
				[map_fmt(row, '<td>%s</td>') for row in self.rows]
		)
		return '<table>%s</table>' % map_fmt(rows, '<tr>%s</tr>')
	
	def _repr_html_(self):
		return html(self)


def as_per_substance_html_table(cont, substances=None, header=None, substance_factory=Substance.from_formula):
	"""

	:param cont:
	:type cont:
	:param substances:
	:type substances:
	:param header:
	:type header:
	:param substance_factory:
	:type substance_factory:

	:return:
	:rtype:
	"""
	
	if substances is None:
		substances = OrderedDict([(k, substance_factory(k)) for k in cont])
	
	def _elem(k):
		try:
			return cont[k]
		except (IndexError, TypeError):
			return cont[list(substances.keys()).index(k)]
	
	rows = [(v.html_name, number_to_scientific_html(_elem(k))) for k, v in substances.items()]
	
	return Table(rows, ['Substance', header or ''])


class _RxnTable:
	"""

	Parameters
	----------
	rsys : ReactionSystem
	sinks_sources_disjoint : tuple, None or True
		Colors sinks & sources. When ``True`` :meth:`sinks_sources_disjoint` is called.
	html_cell_label : Reaction formatting callback
		The function takes an integer, a Reaction instance and a dict of Substances as
		parameters and return a string.

	Returns
	-------
	string: html representation
	list: reactions not considered
	"""
	_rsys_meth = None
	
	def __init__(self, idx_rxn_pairs, substances, colors=None, missing=None, missing_color='eee8aa'):
		self.idx_rxn_pairs = idx_rxn_pairs
		self.substances = substances
		self.colors = colors or {}
		self.missing = missing or []
		self.missing_color = missing_color
	
	@classmethod
	def from_reactionsystem(cls, rsys, color_categories=True):
		idx_rxn_pairs, unconsidered_ri = getattr(rsys, cls._rsys_meth)()
		colors = rsys._category_colors() if color_categories else {}
		missing = [not rsys.substance_participation(sk) for sk in rsys.substances]
		return cls(idx_rxn_pairs, rsys.substances, colors=colors, missing=missing), unconsidered_ri
	
	def _repr_html_(self):
		return css(self, substances=self.substances, colors=self.colors)
	
	def _cell_label_html(self, printer, ori_idx, rxn):
		"""
		Reaction formatting callback. (reaction index -> string) """
		pretty = rxn.unicode(self.substances, with_param=True, with_name=False)
		return '<a title="%d: %s">%s</a>' % (ori_idx, pretty, printer._print(rxn.name or rxn.param))
	
	def _cell_html(self, printer, A, ri, ci=None):
		args = []
		if ci is not None and ri > ci:
			r = '-'
		else:
			if ci is None:  # A is a vector
				c = A[ri]
				is_missing = self.missing[ri]
			else:  # A is a matrix
				c = A[ri][ci]
				is_missing = self.missing[ri] or self.missing[ci]
			
			if c is None:
				r = ''
			else:
				r = ', '.join(self._cell_label_html(printer, *r) for r in c)
			
			if is_missing:
				args.append('style="background-color: #%s;"' % self.missing_color)
		
		return '<td {}>{}</td>'.format(' '.join(args), r)


@append_docstring_from(_RxnTable)
class UnimolecularTable(_RxnTable):
	"""
	Table of unimolecular reactions in a ReactionSystem

	"""
	
	_rsys_meth = '_unimolecular_reactions'
	
	def _html(self, printer, **kwargs):
		if 'substances' not in kwargs:
			kwargs['substances'] = self.substances
		ss = printer._get('substances', **kwargs)
		rows = '\n'.join('<tr><td>{}</td>{}</tr>'.format(
				printer._print(s), self._cell_html(printer, self.idx_rxn_pairs, rowi)
				) for rowi, s in enumerate(ss.values()))
		return f'<table>{rows}</table>'


@append_docstring_from(_RxnTable)
class BimolecularTable(_RxnTable):
	"""
	Table of bimolecular reactions

	"""
	
	_rsys_meth = '_bimolecular_reactions'
	
	def _html(self, printer, **kwargs):
		if 'substances' not in kwargs:
			kwargs['substances'] = self.substances
		ss = printer._get('substances', **kwargs)
		header = '<th></th>' + ''.join(f'<th>{printer._print(s)}</th>' for s in ss.values())
		rows = ['<tr><td>{}</td>{}</tr>'.format(printer._print(s),
												''.join(self._cell_html(printer, self.idx_rxn_pairs, rowi, ci)
														for ci in range(len(ss)))
												) for rowi, s in enumerate(ss.values())]
		return '<table>%s</table>' % '\n'.join([header, '\n'.join(rows)])


def _float_str_w_uncert(x, xe, precision=2):
	"""
	Prints uncertain number with parenthesis

	Parameters
	----------
	x : nominal value
	xe : uncertainty
	precision : number of significant digits in uncertainty

	Examples
	--------
	>>> _float_str_w_uncert(-9.99752e5, 349, 3)
	'-999752(349)'
	>>> _float_str_w_uncert(-9.99752e15, 349e10, 2)
	'-9.9975(35)e15'
	>>> _float_str_w_uncert(3.1416, 0.029, 1)
	'3.14(3)'
	>>> _float_str_w_uncert(3.1416e9, 2.9e6, 1)
	'3.142(3)e9'

	Returns
	-------
	shortest string representation of "x +- xe" either as
	``x.xx(ee)e+xx`` or ``xxx.xx(ee)``

	Notes
	-----
	The code in this function is from a question on StackOverflow:
		http://stackoverflow.com/questions/6671053
		written by:
			Lemming, http://stackoverflow.com/users/841562/lemming
		the code is licensed under 'CC-WIKI'.
		(see: http://blog.stackoverflow.com/2009/06/attribution-required/)

	"""
	
	# base 10 exponents
	x_exp = int(floor(log10(abs(x))))
	xe_exp = int(floor(log10(abs(xe))))
	
	# uncertainty
	un_exp = xe_exp - precision + 1
	un_int = round(xe * 10 ** (-un_exp))
	
	# nominal value
	no_exp = un_exp
	no_int = round(x * 10 ** (-no_exp))
	
	# format - nom(unc)exp
	fieldw = x_exp - no_exp
	fmt = '%%.%df' % fieldw
	result1 = (fmt + '(%.0f)e%d') % (no_int * 10 ** (-fieldw), un_int, x_exp)
	
	# format - nom(unc)
	fieldw = max(0, -no_exp)
	fmt = '%%.%df' % fieldw
	result2 = (fmt + '(%.0f)') % (no_int * 10 ** no_exp, un_int * 10 ** max(0, un_exp))
	
	# return shortest representation
	if len(result2) <= len(result1):
		return result2
	else:
		return result1


def _number_to_X(number, uncertainty, unit, fmt, unit_fmt, fmt_pow_10, space=' '):
	uncertainty = uncertainty or getattr(number, 'uncertainty', None)
	unit = unit or unit_of(number)
	integer_one = 1
	if unit is integer_one:
		unit_str = ''
		mag = number
	else:
		unit_str = space + unit_fmt(unit)
		mag = to_unitless(number, unit)
		if uncertainty is not None:
			uncertainty = to_unitless(uncertainty, unit)
	
	if uncertainty is None:
		if fmt is None:
			fmt = 5
		if isinstance(fmt, int):
			flt = ('%%.%dg' % fmt) % mag
		else:
			flt = fmt(mag)
	else:
		if fmt is None:
			fmt = 2
		if isinstance(fmt, int):
			flt = _float_str_w_uncert(mag, uncertainty, fmt)
		else:
			flt = fmt(mag, uncertainty)
	if 'e' in flt:
		significand, mantissa = flt.split('e')
		return fmt_pow_10(significand, mantissa) + unit_str
	else:
		return flt + unit_str


def _latex_pow_10(significand, mantissa):
	if significand in ('1', '1.0'):
		fmt = '10^{%s}'
	else:
		fmt = significand + r'\cdot 10^{%s}'
	return fmt % str(int(mantissa))


def _unicode_pow_10(significand, mantissa):
	if significand in ('1', '1.0'):
		result = '10'
	else:
		result = significand + '·10'
	return result + ''.join(map(_unicode_sup.get, str(int(mantissa))))


def _html_pow_10(significand, mantissa):
	if significand in ('1', '1.0'):
		result = '10<sup>'
	else:
		result = significand + '&sdot;10<sup>'
	return result + str(int(mantissa)) + '</sup>'

