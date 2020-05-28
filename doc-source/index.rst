=====================
Chemistry Tools
=====================

.. start short_desc

**Python tools for analysis of chemical compounds**

.. end short_desc
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

Installation
----------------

.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			pip install chemistry_tools

	.. tab:: from Anaconda

		First add the required channels

		.. prompt:: bash

			conda config --add channels http://conda.anaconda.org/domdfcoding
			conda config --add channels http://conda.anaconda.org/conda-forge

		Then install

		.. prompt:: bash

			conda install chemistry_tools

	.. tab:: from GitHub

		.. prompt:: bash

			pip install git+https://github.com//chemistry_tools@master

.. end installation


.. toctree::
	:maxdepth: 3
	:caption: API Reference

	api/chemistry_tools
	api/elements
	api/formulae
	api/pubchem

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	Source
	Building

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/chemistry_tools>`__

.. end links