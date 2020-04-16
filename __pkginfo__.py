#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  filename.py
#
#  Copyright (c) 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py

import pathlib

copyright = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

VERSION = "0.2.8"

modname = "chemistry_tools"
py_modules = None
entry_points = None

license = 'LGPL3'

short_desc = 'Python tools for analysis of chemical compounds'

author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/{github_username}/{modname}"

# Get info from files; set: long_description
if pathlib.Path.cwd().name == "doc-source":
	print(pathlib.Path.cwd().parent / "README.rst")
	install_requires = (pathlib.Path.cwd().parent / "requirements.txt").read_text().split("\n")
	long_description = (pathlib.Path.cwd().parent / "README.rst").read_text() + '\n'
else:
	print(pathlib.Path("README.rst"))
	install_requires = pathlib.Path("requirements.txt").read_text().split("\n")
	long_description = pathlib.Path("README.rst").read_text() + '\n'


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
		
		"Topic :: Scientific/Engineering :: Visualization",
		
		"Topic :: Software Development :: Libraries :: Python Modules",
		]
