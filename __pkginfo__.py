#  This file is managed by `git_helper`. Don't edit it directly
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This file is distributed under the same license terms as the program it came with.
#  There will probably be a file called LICEN[S/C]E in the same directory as this file.
#
#  In any case, this program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py
#

# stdlib
import pathlib

__all__ = [
		"__copyright__",
		"__version__",
		"modname",
		"pypi_name",
		"py_modules",
		"entry_points",
		"__license__",
		"short_desc",
		"author",
		"author_email",
		"github_username",
		"web",
		"github_url",
		"project_urls",
		"repo_root",
		"long_description",
		"install_requires",
		"extras_require",
		"classifiers",
		"keywords",
		"import_name",
		]

__copyright__ = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "0.3.1"

modname = "chemistry_tools"
pypi_name = "chemistry_tools"
import_name = "chemistry_tools"
py_modules = []
entry_points = {
		"console_scripts": []
		}

__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"

short_desc = "Python tools for analysis of chemical compounds"

__author__ = author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/domdfcoding/chemistry_tools"
project_urls = {
		"Documentation": f"https://chemistry_tools.readthedocs.io",
		"Issue Tracker": f"{github_url}/issues",
		"Source Code": github_url,
		}

repo_root = pathlib.Path(__file__).parent

# Get info from files; set: long_description
long_description = (repo_root / "README.rst").read_text().replace("0.3.1", __version__) + '\n'
conda_description = """Python tools for analysis of chemical compounds


Before installing please ensure you have added the following channels: domdfcoding, conda-forge"""
__all__.append("conda_description")

install_requires = (repo_root / "requirements.txt").read_text().split('\n')
extras_require = {'pubchem': ['memoized_property>=1.0.3', 'tabulate>=0.8.3', 'aenum>=2.2.3', 'domdf_python_tools>=0.3.4', 'Pillow>=7.0.0', 'cawdrey>=0.1.5', 'pyparsing>=2.2.0', 'mathematical>=0.1.7'], 'elements': ['domdf_python_tools>=0.3.4', 'memoized-property>=1.0.3'], 'formulae': ['aenum>=2.2.3', 'tabulate>=0.8.3', 'cawdrey>=0.1.5', 'pyparsing>=2.2.0', 'mathematical>=0.1.7', 'domdf_python_tools>=0.3.4', 'memoized-property>=1.0.3'], 'plotting': ['matplotlib>=3.0.0'], 'toxnet': ['beautifulsoup4>=4.7.0'], 'all': ['Pillow>=7.0.0', 'aenum>=2.2.3', 'beautifulsoup4>=4.7.0', 'cawdrey>=0.1.5', 'domdf_python_tools>=0.3.4', 'mathematical>=0.1.7', 'matplotlib>=3.0.0', 'memoized-property>=1.0.3', 'memoized_property>=1.0.3', 'pyparsing>=2.2.0', 'tabulate>=0.8.3']}

classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Database :: Front-Ends',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Topic :: Scientific/Engineering :: Chemistry',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3 :: Only',
		'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

		]

keywords = ""
