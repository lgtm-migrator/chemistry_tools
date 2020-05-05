#!/usr/bin/env python
"""Setup script"""

from __pkginfo__ import (
	author, author_email, install_requires,
	license, long_description, classifiers,
	entry_points, modname, py_modules,
	short_desc, VERSION, web, project_urls,
	pubchem_requires, formulae_requires,
	elements_requires, plotting_requires,
	)

from setuptools import setup, find_packages

setup(
		author=author,
		author_email=author_email,
		classifiers=classifiers,
		description=short_desc,
		entry_points=entry_points,
		install_requires=install_requires,
		extras_require={
				"pubchem":  pubchem_requires,
				"elements":  elements_requires,
				"formulae":  formulae_requires,
				"plotting":  plotting_requires,
				"all":  pubchem_requires + elements_requires + formulae_requires + plotting_requires,
				},
		license=license,
		long_description=long_description,
		name=modname,
		packages=find_packages(exclude=("tests",)),
		py_modules=py_modules,
		url=web,
		project_urls=project_urls,
		version=VERSION,
		python_requires=">=3.6",
		include_package_data=True,
		)
