#  This file is managed by 'repo_helper'. Don't edit it directly.
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

__all__ = [
		"__version__",
		"extras_require",
		]

__version__ = "0.4.1"
extras_require = {
		"pubchem": [
				"cawdrey>=0.1.7", "mathematical>=0.1.13", "pillow>=7.0.0", "pyparsing>=2.2.0", "tabulate>=0.8.9"
				],
		"formulae": ["cawdrey>=0.1.7", "mathematical>=0.1.13", "pyparsing>=2.2.0", "tabulate>=0.8.9"],
		"plotting": [
				'matplotlib>=3.0.0; platform_machine != "aarch64" or python_version > "3.6"',
				'matplotlib<=3.2.2; platform_machine == "aarch64" and python_version == "3.6"'
				],
		"toxnet": ["beautifulsoup4>=4.7.0"],
		"all": [
				"beautifulsoup4>=4.7.0",
				"cawdrey>=0.1.7",
				"mathematical>=0.1.13",
				'matplotlib>=3.0.0; platform_machine != "aarch64" or python_version > "3.6"',
				'matplotlib<=3.2.2; platform_machine == "aarch64" and python_version == "3.6"',
				"pillow>=7.0.0",
				"pyparsing>=2.2.0",
				"tabulate>=0.8.9"
				]
		}
