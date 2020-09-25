#!/usr/bin/env python
#
#  compound.py
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
import json
from collections import Counter
from itertools import zip_longest

# 3rd party
from memoized_property import memoized_property

# this package
from chemistry_tools.constants import CoordinateType
from chemistry_tools.elements import ELEMENTS
from chemistry_tools.property_format import *
from chemistry_tools.pubchem.atom import Atom
from chemistry_tools.pubchem.bond import Bond
from chemistry_tools.pubchem.errors import ResponseParseError
from chemistry_tools.toxnet import toxnet

# this package
from .compoundv2 import Compound as CompoundV2
from .utils import get_full_json, get_json, request


class PhysicalProperties:
	"""
	Corresponds to a single record from the PubChem Compound database.

	The PubChem Compound database is constructed from the Substance database
	using a standardization and deduplication process.
	Each Compound is uniquely identified by a CID.
	"""

	def __init__(self, cid):
		"""
		Initialize with a record dict from the PubChem PUG REST service.

		For most users, the ``from_cid()`` class method is probably a better way of creating Compounds.

		:param record: A compound record returned by the PubChem PUG REST service.
		"""

		self.cid = cid

		print(f'Created {self}')
		self._view_record = get_full_json(self.cid)

		self.hazards = []  # COSHH Hazards
		self.CAS = ''
		self._physical_properties = {}  # Physical Properties (dictionary)
		self._view_record = get_full_json(self.cid)
		self._parse_view_record()

	@property
	def view_record(self):
		return self._view_record

	def _parse_view_record(self):
		try:
			for record in self.view_record["Record"]["Section"]:
				if record["TOCHeading"] == "Chemical Safety":
					try:
						for hazard in record["Information"][0]["Value"]["StringWithMarkup"][0]["Markup"]:
							self.hazards.append(hazard["Extra"])
					except KeyError:
						pass
				#
				# elif record["TOCHeading"] == "Chemical and Physical Properties":
				# 	for section in record["Section"]:
				# 		if section["TOCHeading"] == "Computed Properties":
				# 			for physical_property in section["Section"]:
				# 				name = physical_property["TOCHeading"]
				# 				self._physical_properties[name] = {}
				# 				self._physical_properties[name]["Description"] = physical_property[
				# 					"Description"]
				#
				# 				try:
				# 					self._physical_properties[name]["Value"] = Decimal(
				# 							str(physical_property["Information"][0]["Value"]["Number"][0]))
				# 				except KeyError:
				# 					value = physical_property["Information"][0]["Value"]["StringWithMarkup"][0][
				# 						"String"]
				# 					if value == "Yes":
				# 						value = True
				# 					elif value == "No":
				# 						value = False
				#
				# 					self._physical_properties[name]["Value"] = value
				#
				# 				try:
				# 					self._physical_properties[name]["Unit"] = \
				# 						physical_property["Information"][0]["Value"]["Unit"]
				# 				except KeyError:
				# 					self._physical_properties[name]["Unit"] = None
				#
				# 		elif section["TOCHeading"] == "Experimental Properties":
				# 			# First Try TOXNET
				# 			try:
				# 				self._physical_properties = {**self._physical_properties, **toxnet(self.CAS)}
				# 			except ValueError:  # Not Found in TOXNET
				# 				# import traceback
				# 				# traceback.print_exc()
				# 				pass
				# 			for physical_property in section["Section"]:
				# 				name = physical_property["TOCHeading"]
				#
				# 				if name == "Other Experimental Properties":
				# 					name = "Other Chemical/Physical Properties"
				# 				elif name == "LogKoa":
				# 					name = "Octanol/Water Partition Coefficient"
				# 				elif name == "Density":
				# 					name = "Density/Specific Gravity"
				#
				# 				if (name in self._physical_properties) or (
				# 						name in ["Molecular Formula", "Molecular Weight", "Physical Description"]):
				# 					continue
				#
				# 				self._physical_properties[name] = {}
				# 				self._physical_properties[name]["Description"] = physical_property[
				# 					"Description"]
				#
				# 				# TODO: Skip Physical Description, :
				# 				try:
				# 					self._physical_properties[name]["Value"] = Decimal(
				# 							str(physical_property["Information"][0]["Value"]["Number"][0]))
				# 				except KeyError:
				# 					value = property_format(
				# 							physical_property["Information"][0]["Value"]["StringWithMarkup"][0][
				# 								"String"])
				# 					if value == "Yes":
				# 						value = True
				# 					elif value == "No":
				# 						value = False
				#
				# 					self._physical_properties[name]["Value"] = value
				#
				# 				try:
				# 					self._physical_properties[name]["Unit"] = \
				# 						physical_property["Information"][0]["Value"]["Unit"]
				# 				except KeyError:
				# 					self._physical_properties[name]["Unit"] = None
				# 		# import pprint
				# 		# pprint.pprint(self._physical_properties)

				elif record["TOCHeading"] == "Names and Identifiers":
					for section in record["Section"]:
						if section["TOCHeading"] == "Record Description":
							for description in section["Information"]:
								try:
									if description["Description"] == "Physical Description":
										self.physical_description = description["Value"]["StringWithMarkup"][0]

									elif description["Description"] == "Ontology Summary":
										self.ontology = description["Value"]["StringWithMarkup"][0]

									elif description["Description"] == "Metabolite Description":
										self.metabolite = description["Value"]["StringWithMarkup"][0]
								except KeyError:
									pass

						elif section["TOCHeading"] == "Computed Descriptors":
							for subsection in section["Section"]:
								if subsection["TOCHeading"] == "IUPAC Name":
									self.IUPAC = subsection["Information"][0]["Value"]["StringWithMarkup"][0]

						elif section["TOCHeading"] == "Other Identifiers":
							for subsection in section["Section"]:
								if subsection["TOCHeading"] == "CAS":
									self.CAS = subsection["Information"][0]["Value"]["StringWithMarkup"][0][
											"String"]

		except KeyError:
			pass

	"""
	.. note::

		When searching using a SMILES or InChI query that is not present in the PubChem Compound database, an
		automatically generated record may be returned that contains properties that have been calculated on the
		fly. These records will not have a CID prop.
	"""

	def get_property_description(self, prop):
		try:
			return self.get_property(prop)["Description"]
		except KeyError:
			return

	def get_property_value(self, prop):
		try:
			return self.get_property(prop)["Value"]
		except KeyError:
			return "NotFound"

	def get_property_unit(self, prop):
		try:
			return self.get_property(prop)["Unit"]
		except KeyError:
			return

	def get_property(self, prop):
		# TODO Error handling
		try:
			return self._physical_properties[prop]
		except KeyError:
			return {"Value": "NotFound", "Unit": None, "Description": None}

	#
	# # TOXNET / Experimental Properties
	#
	# @property
	# def boiling_point(self):
	# 	"""Boiling Point"""
	# 	return self.get_property_value("Boiling Point")
	#
	# @property
	# def color(self):
	# 	"""Color/Form"""
	# 	return self.get_property_value("Color/Form")
	#
	# @property
	# def density(self):
	# 	"""Density/Specific Gravity"""
	# 	return self.get_property_value("Density/Specific Gravity")
	#
	# @property
	# def specific_gravity(self):
	# 	"""Density/Specific Gravity"""
	# 	return self.get_property_value("Density/Specific Gravity")
	#
	# @property
	# def dissociation_constant(self):
	# 	"""Dissociation Constants"""
	# 	return self.get_property_value("Dissociation Constants")
	#
	# @property
	# def heat_combustion(self):
	# 	"""Heat of Combustion"""
	# 	return self.get_property_value("Heat of Combustion")
	#
	# @property
	# def melting_point(self):
	# 	"""Melting Point"""
	# 	return self.get_property_value("Melting Point")
	#
	# @property
	# def partition_coeff(self):
	# 	"""Octanol/Water Partition Coefficient"""
	# 	return self.get_property_value("Octanol/Water Partition Coefficient")
	#
	# @property
	# def odor(self):
	# 	"""Odor"""
	# 	return self.get_property_value("Odor")
	#
	# @property
	# def other_props(self):
	# 	"""Other Chemical/Physical Properties"""
	# 	return self.get_property_value("Other Chemical/Physical Properties")
	#
	# @property
	# def solubility(self):
	# 	"""Solubility"""
	# 	return self.get_property_value("Solubility")
	#
	# @property
	# def spectral_props(self):
	# 	"""Spectral Properties"""
	# 	return self.get_property_value("Spectral Properties")
	#
	# @property
	# def surface_tension(self):
	# 	"""Surface Tension"""
	# 	return self.get_property_value("Surface Tension")
	#
	# @property
	# def vapor_density(self):
	# 	"""Vapor Density"""
	# 	return self.get_property_value("Vapor Density")
	#
	# @property
	# def vapor_pressure(self):
	# 	"""Vapor Pressure"""
	# 	return self.get_property_value("Vapor Pressure")
