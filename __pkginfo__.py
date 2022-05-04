#  This file is managed by 'repo_helper'. Don't edit it directly.

__all__ = ["extras_require"]

extras_require = {
		"pubchem": [
				"cawdrey>=0.1.7",
				"mathematical>=0.1.13",
				'pillow>=7.0.0; platform_python_implementation == "PyPy" and python_version >= "3.8" and platform_system == "Windows"',
				'pillow>=7.0.0; platform_python_implementation == "PyPy" and python_version >= "3.7" and platform_system != "Windows"',
				'pillow>=7.0.0; platform_python_implementation != "PyPy"',
				'pillow<9.0.0,>=7.0.0; platform_python_implementation == "PyPy" and python_version == "3.7" and platform_system == "Windows"',
				'pillow<8.0.0,>=7.0.0; platform_python_implementation == "PyPy" and python_version == "3.6"',
				"pyparsing>=2.4.6",
				"tabulate>=0.8.9"
				],
		"formulae": ["cawdrey>=0.1.7", "mathematical>=0.1.13", "pyparsing>=2.4.6", "tabulate>=0.8.9"],
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
				'pillow>=7.0.0; platform_python_implementation == "PyPy" and python_version >= "3.8" and platform_system == "Windows"',
				'pillow>=7.0.0; platform_python_implementation == "PyPy" and python_version >= "3.7" and platform_system != "Windows"',
				'pillow>=7.0.0; platform_python_implementation != "PyPy"',
				'pillow<9.0.0,>=7.0.0; platform_python_implementation == "PyPy" and python_version == "3.7" and platform_system == "Windows"',
				'pillow<8.0.0,>=7.0.0; platform_python_implementation == "PyPy" and python_version == "3.6"',
				"pyparsing>=2.4.6",
				"tabulate>=0.8.9"
				]
		}
