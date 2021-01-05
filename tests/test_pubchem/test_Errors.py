"""
test_Errors
~~~~~~~~~~~~~

Test Errors.

"""

# 3rd party
import pytest

# this package
from chemistry_tools.pubchem.compound import Compound
from chemistry_tools.pubchem.errors import BadRequestError, NotFoundError
from chemistry_tools.pubchem.lookup import get_compounds


def test_invalid_identifier(pubchem_cassette):
	"""
	BadRequestError should be raised if identifier is not a positive integer.
	"""

	with pytest.raises(BadRequestError):
		Compound.from_cid("aergaerhg")
	with pytest.raises(NotFoundError):
		get_compounds("srthrthsr")


def test_notfound_identifier(pubchem_cassette):
	"""
	NotFoundError should be raised if identifier is a positive integer but record doesn't exist.
	"""

	with pytest.raises(NotFoundError):
		Compound.from_cid(999999999)
	with pytest.raises(NotFoundError):
		get_compounds(999999999, "cid")
