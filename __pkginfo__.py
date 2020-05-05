# Copyright (C) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py


import pathlib

copyright = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

VERSION = "0.2.9"

modname = "chemistry_tools"
py_modules = None
entry_points = None

license = 'LGPL3'

short_desc = 'Python tools for analysis of chemical compounds'

author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/{github_username}/{modname}"
project_urls = {
		"Documentation": f"https://{modname}.readthedocs.io",  # TODO: Make this link match the package version
		"Issue Tracker": f"{github_url}/issues",
		"Source Code": github_url,
		}

if pathlib.Path.cwd().name == "doc-source":
	repo_root = pathlib.Path.cwd().parent
else:
	repo_root = pathlib.Path.cwd()

pkg_root = repo_root / "chemistry_tools"

# Get info from files; set: long_description
print(repo_root / "README.rst")
install_requires = (repo_root / "requirements.txt").read_text().split("\n")
pubchem_requires = (pkg_root / "pubchem" / "requirements.txt").read_text().split("\n")
formulae_requires = (pkg_root / "formulae" / "requirements.txt").read_text().split("\n")
elements_requires = (pkg_root / "elements" / "requirements.txt").read_text().split("\n")
long_description = (repo_root / "README.rst").read_text() + '\n'
plotting_requires = ["matplotlib>=3.0.0"]

classifiers = [
		# "Development Status :: 1 - Planning",
		# "Development Status :: 2 - Pre-Alpha",
		"Development Status :: 3 - Alpha",
		# "Development Status :: 4 - Beta",
		# "Development Status :: 5 - Production/Stable",
		# "Development Status :: 6 - Mature",
		# "Development Status :: 7 - Inactive",
		
		"Operating System :: OS Independent",
		
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		
		"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
		
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: Implementation :: CPython",
		
		"Topic :: Database :: Front-Ends",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Scientific/Engineering :: Chemistry",
		# "Topic :: Scientific/Engineering :: Visualization",
		"Topic :: Software Development :: Libraries :: Python Modules",
		]
