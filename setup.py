from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="chemistry_tools",
	version="0.1.0",
    author='Dominic Davis-Foster',
	author_email="dominic@davis-foster.co.uk",
	packages=find_packages(),
	url="https://github.com/domdfcoding/chemistry_tools",
	description='Python tools for analysis of chemical compounds',
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta",
		'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
		"Topic :: Scientific/Engineering :: Visualization",
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
		
    ],
	install_requires=[
		"numpy >= 1.16.0",
		"pandas >= 0.24.0",
		"matplotlib >= 3.0.0",
		"requests >= 2.21.0",
		"beautifulsoup4 >= 4.7.0",
	],
)
