****************
chemistry_tools
****************

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 
	
.. |docs| image:: https://readthedocs.org/projects/chemistry_tools/badge/?version=latest
	:target: https://chemistry_tools.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/chemistry_tools/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/chemistry_tools
	:alt: Travis Build Status
	
.. |requires| image:: https://requires.io/github/domdfcoding/chemistry_tools/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/chemistry_tools/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://coveralls.io/repos/github/domdfcoding/chemistry_tools/badge.svg?branch=master
	:target: https://coveralls.io/github/domdfcoding/chemistry_tools?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/chemistry_tools
	:target: https://www.codefactor.io/repository/github/domdfcoding/chemistry_tools
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/chemistry_tools.svg
	:target: https://pypi.org/project/chemistry_tools/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/chemistry_tools.svg
	:target: https://pypi.org/project/chemistry_tools/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/chemistry_tools
	:target: https://pypi.org/project/chemistry_tools/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/chemistry_tools
	:target: https://pypi.org/project/chemistry_tools/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/chemistry_tools
	:alt: Conda - Package Version
	:target: https://anaconda.org/domdfcoding/chemistry_tools

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/chemistry_tools?label=conda%7Cplatform
	:alt: Conda - Platform
	:target: https://anaconda.org/domdfcoding/chemistry_tools

.. |license| image:: https://img.shields.io/github/license/domdfcoding/chemistry_tools
	:alt: License
	:target: https://github.com/domdfcoding/chemistry_tools/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/chemistry_tools
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/chemistry_tools/v0.3.0
	:target: https://github.com/domdfcoding/chemistry_tools/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/chemistry_tools
	:target: https://github.com/domdfcoding/chemistry_tools/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields


Python tools for analysis of chemical compounds


lookup and pubchem adapted from PubChemPy
=========================================
Python interface to the PubChem REST API

|

Copyright 2017 Matt Swain <m.swain@me.com>

https://github.com/mcs07/PubChemPy

Available under the MIT License


SpectrumSimilarity
======================================
Perform mass spectrum similarity calculations

|

Adapted from SpectrumSimilarity.R

Part of OrgMassSpecR

Copyright 2011-2017 Nathan Dodder <nathand@sccwrp.org>

https://cran.r-project.org/web/packages/OrgMassSpecR/index.html

Available under the BSD 2-Clause License


elements and formulae
=========================

Provides properties for the elements in the periodic table, and functions
for parsing formulae and calculating isotope distributions.

Calculations are based on the isotopic composition of the elements. Mass
deficiency due to chemical bonding is not taken into account.

Examples of valid formulae are ``H2O``, ``[2H]2O``, ``CH3COOH``, ``EtOH``,
``CuSO4.5H2O``, and ``(COOH)2``. Formulae are case sensitive.

|

Based on ChemPy (https://github.com/bjodah/chempy)

Copyright (c) 2015-2018, Björn Dahlgren

All rights reserved.

|

Also based on molmass (https://github.com/cgohlke/molmass)

Copyright (c) 1990-2020, Christoph Gohlke

All rights reserved.

Licensed under the BSD 3-Clause License

|

Also based on Pyteomics (https://github.com/levitsky/pyteomics)

Copyright (c) 2011-2015, Anton Goloborodko & Lev Levitsky

Licensed under the Apache License

