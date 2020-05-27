#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  properties.py
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
import warnings
from collections import namedtuple
from textwrap import dedent
from typing import Any

# 3rd party
from tabulate import tabulate

# this package
from chemistry_tools.formulae import Formula
from .enums import PubChemFormats, PubChemNamespace
from .pug_rest import _do_rest_get
from .utils import _force_sequence_or_csv

PropData = namedtuple("PropData", "name, description, type, attr_name")

_properties = [
		PropData("MolecularFormula", "Molecular formula.", Formula.from_string, "molecular_formula"),
		PropData(
				"MolecularWeight",
				"The molecular weight is the sum of all atomic weights of the constituent atoms "
				"in a compound, measured in g/mol. In the absence of explicit isotope labelling, "
				"averaged natural abundance is assumed. If an atom bears an explicit isotope label, "
				"100% isotopic purity is assumed at this location.",
				float,
				"molecular_weight"
				),
		PropData(
				"CanonicalSMILES",
				"Canonical SMILES (Simplified Molecular Input Line Entry System) string. "
				"It is a unique SMILES string of a compound, generated by a “canonicalization” algorithm.",
				str,
				"canonical_smiles"
				),
		PropData(
				"IsomericSMILES",
				"Isomeric SMILES string.  It is a SMILES string with stereochemical and isotopic specifications.",
				str,
				"isomeric_smiles"
				),
		PropData(
				"InChI",
				"Standard IUPAC International Chemical Identifier (InChI). It does not allow for user "
				"selectable options in dealing with the stereochemistry and tautomer layers of the InChI string.",
				str,
				"inchi"
				),
		PropData(
				"InChIKey",
				"Hashed version of the full standard InChI, consisting of 27 characters.",
				str,
				"inchikey"
				),
		PropData(
				"IUPACName",
				"Chemical name systematically determined according to the IUPAC nomenclatures.",
				str,
				"iupac_name"
				),
		PropData(
				"XLogP",
				"Computationally generated octanol-water partition coefficient or distribution coefficient. "
				"XLogP is used as a measure of hydrophilicity or hydrophobicity of a molecule.",
				float,
				"xlogp"
				),
		PropData(
				"ExactMass",
				"The mass of the most likely isotopic composition for a single molecule, corresponding "
				"to the most intense ion/molecule peak in a mass spectrum.",
				float,
				"exact_mass"
				),
		PropData(
				"MonoisotopicMass",
				"The mass of a molecule, calculated using the mass of the most abundant isotope of each element.",
				float,
				"monoisotopic_mass"
				),
		PropData(
				"TPSA",
				"Topological polar surface area, computed by the algorithm described in the paper by Ertl et al.",
				float,
				"tpsa"
				),
		PropData(
				"Complexity",
				"The molecular complexity rating of a compound, computed using the Bertz/Hendrickson/Ihlenfeldt formula.",
				float,
				"complexity"
				),
		PropData("Charge", "The total (or net) charge of a molecule.", int, "charge"),
		PropData("HBondDonorCount", "Number of hydrogen-bond donors in the structure.", int, "h_bond_donor_count"),
		PropData(
				"HBondAcceptorCount",
				"Number of hydrogen-bond acceptors in the structure.",
				int,
				"h_bond_acceptor_count"
				),
		PropData("RotatableBondCount", "Number of rotatable bonds.", int, "rotatable_bond_count"),
		PropData("HeavyAtomCount", "Number of non-hydrogen atoms.", int, "heavy_atom_count"),
		PropData("IsotopeAtomCount", "Number of atoms with enriched isotope(s)", int, "isotope_atom_count"),
		PropData(
				"AtomStereoCount",
				"Total number of atoms with tetrahedral (sp3) stereo [e.g., (R)- or (S)-configuration]",
				int,
				"atom_stereo_count"
				),
		PropData(
				"DefinedAtomStereoCount",
				"Number of atoms with defined tetrahedral (sp3) stereo.",
				int,
				"defined_atom_stereo_count"
				),
		PropData(
				"UndefinedAtomStereoCount",
				"Number of atoms with undefined tetrahedral (sp3) stereo.",
				int,
				"undefined_atom_stereo_count"
				),
		PropData(
				"BondStereoCount",
				"Total number of bonds with planar (sp2) stereo [e.g., (E)- or (Z)-configuration].",
				int,
				"bond_stereo_count"
				),
		PropData(
				"DefinedBondStereoCount",
				"Number of atoms with defined planar (sp2) stereo.",
				int,
				"defined_bond_stereo_count"
				),
		PropData(
				"UndefinedBondStereoCount",
				"Number of atoms with undefined planar (sp2) stereo.",
				int,
				"undefined_bond_stereo_count"
				),
		PropData("CovalentUnitCount", "Number of covalently bound units.", int, "covalent_unit_count"),
		PropData(
				"Volume3D",
				"Analytic volume of the first diverse conformer (default conformer) for a compound.",
				str,
				"volume3d"
				),
		PropData(
				"XStericQuadrupole3D",
				"The x component of the quadrupole moment (Qx) of the first diverse conformer (default conformer) "
				"for a compound.",
				float,
				"volume_3d"
				),
		PropData(
				"YStericQuadrupole3D",
				"The y component of the quadrupole moment (Qy) of the first diverse conformer (default conformer) "
				"for a compound.",
				float,
				"x_steric_quadrupole_3d"
				),
		PropData(
				"ZStericQuadrupole3D",
				"The z component of the quadrupole moment (Qz) of the first diverse conformer (default conformer) "
				"for a compound.",
				float,
				"y_steric_quadrupole_3d"
				),
		PropData(
				"FeatureCount3D",
				"Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, "
				"FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)",
				int,
				"feature_count_3d"
				),
		PropData(
				"FeatureAcceptorCount3D",
				"Number of hydrogen-bond acceptors of a conformer.",
				int,
				"feature_acceptor_count_3d"
				),
		PropData(
				"FeatureDonorCount3D",
				"Number of hydrogen-bond donors of a conformer.",
				int,
				"feature_donor_count_3d"
				),
		PropData(
				"FeatureAnionCount3D",
				"Number of anionic centers (at pH 7) of a conformer.",
				int,
				"feature_anion_count_3d"
				),
		PropData(
				"FeatureCationCount3D",
				"Number of cationic centers (at pH 7) of a conformer.",
				int,
				"feature_cation_count_3d"
				),
		PropData("FeatureRingCount3D", "Number of rings of a conformer.", int, "feature_ring_count_3d"),
		PropData(
				"FeatureHydrophobeCount3D",
				"Number of hydrophobes of a conformer.",
				int,
				"feature_hydrophobe_count_3d"
				),
		PropData("ConformerModelRMSD3D", "Conformer sampling RMSD in Å.", float, "conformer_model_rmsd_3d"),
		PropData(
				"EffectiveRotorCount3D",
				"Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, "
				"FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)",
				int,
				"effective_rotor_count_3d"
				),
		PropData(
				"ConformerCount3D",
				"The number of conformers in the conformer model for a compound.",
				int,
				"conformer_count_3d"
				),
		PropData(
				"Fingerprint2D",
				"Base64-encoded PubChem Substructure Fingerprint of a molecule.",
				str,
				"fingerprint_2d"
				),
		]

valid_property_descriptions = tabulate([(prop.name, prop.description) for prop in _properties],
										headers=["Property", "Description"])

# Properties for PubChem REST API
valid_properties = {prop.name: prop.type for prop in _properties}

# Allows properties to optionally be specified as underscore_separated, consistent with Compound attributes
PROPERTY_MAP = {prop.attr_name: prop.name for prop in _properties}


def insert_valid_properties_table():

	def wrapper(target):
		deindented_doc = dedent(target.__doc__)

		replaced_doc = deindented_doc.replace(
				":: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::",
				valid_property_descriptions
				)

		target.__doc__ = replaced_doc

		return target

	return wrapper


@insert_valid_properties_table()
def rest_get_properties_json(identifier, namespace=PubChemNamespace.name, properties='', **kwargs):
	"""
	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`
	:type namespace: PubChemNamespace, optional
	:param properties: The properties to retrieve for the compound. See the table below. Can be either a comma-separated string or a list.

	:: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::

	:type properties: str, Sequence[str]
	:param **kwargs: Optional arguments that ``json.loads`` takes.
	:raises ValueError: If the response body does not contain valid json.

	:return: Parsed json data
	:rtype: dict
	"""

	properties = _force_valid_properties(properties)

	for prop in properties:
		if prop not in valid_properties:
			raise ValueError(f"Unknown property '{prop}'")

	return _do_rest_get(namespace, identifier, domain=f"property/{','.join(properties)}").json(**kwargs)


@insert_valid_properties_table()
def rest_get_properties(identifier, namespace=PubChemNamespace.name, properties='', format_=PubChemFormats.CSV):
	"""
	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`
	:type namespace: PubChemNamespace, optional
	:param properties: The properties to retrieve for the compound. See the table below. Can be either a comma-separated string or a list.

	:: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::

	:type properties: str, Sequence[str]
	:param **kwargs: Optional arguments that ``json.loads`` takes.
	:raises ValueError: If the response body does not contain valid json.

	:return:
	:rtype:
	"""

	properties = _force_valid_properties(properties)

	for prop in properties:
		if prop not in valid_properties:
			raise ValueError(f"Unknown property '{prop}'")

	return _do_rest_get(namespace, identifier, domain=f"property/{','.join(properties)}", format_=format_).text


def _force_valid_properties(properties):
	properties = _force_sequence_or_csv(properties, "properties")

	ordered_properties = []

	for prop in valid_properties:
		if prop in properties:
			properties.remove(prop)
			ordered_properties.append(prop)

	if properties:
		raise ValueError(f"Unknown properties '{', '.join(properties)}'")

	if not ordered_properties:
		raise ValueError(f"Please supply one or more properties")

	return ordered_properties


@insert_valid_properties_table()
def get_properties(identifier, properties='', namespace="name", as_dataframe=False):
	"""
	Returns the requested properties for the compound with the given identifier.
	As more than one compound may be identified the results are returned in a list.

	:param identifier: Identifiers (e.g. name, CID) for the compound to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]

	:param properties: The properties to retrieve for the compound. See the table below. Can be either a comma-separated string or a list.

	:: See chemistry_tools.pubchem.properties.valid_property_descriptions for a list of valid properties ::

	:type properties: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`. Default "name"
	:type namespace: PubChemNamespace, optional
	:param as_dataframe: Automatically extract the properties into a pandas :class:`~pandas.DataFrame`.
	:type as_dataframe: bool, optional

	:raises ValueError: If the response body does not contain valid json.

	:return: List of dictionaries mapping properties to values
	:rtype: List[dict]
	"""

	if isinstance(properties, str) and properties.lower() == "all":
		properties = list(valid_properties.keys())

	properties = _force_valid_properties(properties)

	data = rest_get_properties_json(identifier, namespace, properties)

	results = []

	for compound in parse_properties(data):
		parsed_data = {"CID": compound["CID"]}

		for prop in properties:
			parsed_data[prop] = compound[prop]

		results.append(parsed_data)

	if as_dataframe:
		import pandas as pd
		return pd.DataFrame.from_records(results, index='CID')

	return results


def parse_properties(property_data):
	"""
	Parse raw data from the ``property`` endpoint of the REST API

	:param property_data:
	:type property_data: dict

	:return: A list of dictionaries mapping the properties to values for each compound
	:rtype: list[dict]
	"""

	compounds = {}
	fields = valid_properties

	for entry in property_data["PropertyTable"]["Properties"]:

		cid = entry["CID"]

		if cid not in compounds:
			compounds[cid] = {var: None for var in fields}
			compounds[cid]["CID"] = cid

		for var in fields:
			if var in entry:
				property_type = valid_properties[var]

				if property_type is int and isinstance(entry[var], float):
					warnings.warn(f"Loss of precision converting {var} from float to int.")

				if property_type is not Any:
					compounds[cid][var] = property_type(entry[var])
				else:
					compounds[cid][var] = entry[var]

	return list(compounds.values())


class PubChemProperty(namedtuple("__BasePubChemProperty", "label name value dtype source")):
	__slots__ = []

	def __new__(cls, label, name=None, value=None, dtype=None, source=None):
		if source is None:
			source = {}

		if dtype:
			value = dtype(value)
		label = str(label)
		if name:
			name = str(name)

		return super().__new__(cls, label, name, value, dtype, source)


def string_list(val):
	return [str(x) for x in val]


def _parse_record_property(prop):
	urn = prop["urn"]

	if "name" in urn:
		prop_name = urn["name"]
	else:
		prop_name = None

	dtype = urn["datatype"]

	if dtype == 7:
		prop_dtype = float
		val_key = "fval"
	elif dtype == 1:
		prop_dtype = str
		val_key = "sval"
	elif dtype == 16:
		prop_dtype = str
		val_key = "binary"
	elif dtype == 5:
		prop_dtype = int
		val_key = "ival"
	elif dtype == 2:
		prop_dtype = string_list
		val_key = "slist"
	else:
		raise ValueError(f"Unknown datatype '{dtype}' for property {prop_name} {urn['label']}")

	value = prop["value"][val_key]

	prop_source = {k: val for k, val in urn.items() if k not in {"datatype", "label", "name"}}

	return PubChemProperty(label=urn["label"], name=prop_name, value=value, dtype=prop_dtype, source=prop_source)
