#  This file is managed by 'repo_helper'. Don't edit it directly.
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
		"__license__",
		"__author__",
		"short_desc",
		"author",
		"author_email",
		"github_username",
		"web",
		"github_url",
		"repo_root",
		"install_requires",
		"extras_require",
		"project_urls",

		"import_name",
		]

__copyright__ = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "0.3.1"
modname = "chemistry_tools"
pypi_name = "chemistry_tools"
import_name = "chemistry_tools"
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
short_desc = 'Python tools for analysis of chemical compounds.'
__author__ = author = 'Dominic Davis-Foster'
author_email = 'dominic@davis-foster.co.uk'
github_username = "domdfcoding"
web = github_url = "https://github.com/domdfcoding/chemistry_tools"
repo_root = pathlib.Path(__file__).parent
install_requires = (repo_root / "requirements.txt").read_text(encoding="utf-8").split('\n')
extras_require = {'pubchem': ['cawdrey>=0.1.5', 'domdf_python_tools>=0.3.6', 'mathematical>=0.1.7', 'memoized-property>=1.0.3', 'Pillow>=7.0.0', 'pyparsing>=2.2.0', 'tabulate>=0.8.3'], 'elements': ['domdf_python_tools>=0.3.6', 'memoized-property>=1.0.3'], 'formulae': ['cawdrey>=0.1.5', 'domdf_python_tools>=0.3.6', 'mathematical>=0.1.7', 'memoized-property>=1.0.3', 'pyparsing>=2.2.0', 'tabulate>=0.8.3'], 'plotting': ['matplotlib>=3.0.0'], 'toxnet': ['beautifulsoup4>=4.7.0'], 'all': ['Pillow>=7.0.0', 'beautifulsoup4>=4.7.0', 'cawdrey>=0.1.5', 'domdf_python_tools>=0.3.6', 'mathematical>=0.1.7', 'matplotlib>=3.0.0', 'memoized-property>=1.0.3', 'pyparsing>=2.2.0', 'tabulate>=0.8.3']}



conda_description = """Python tools for analysis of chemical compounds.


Before installing please ensure you have added the following channels: domdfcoding, conda-forge"""
__all__.append("conda_description")


project_urls = {
		"Documentation": "https://chemistry_tools.readthedocs.io",
		"Issue Tracker": f"{github_url}/issues",
		"Source Code": github_url,
		}
