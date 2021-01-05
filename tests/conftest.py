# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus

# this package
from chemistry_tools import cached_requests

pytest_plugins = ("domdf_python_tools.testing", )

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def pubchem_cassette(request: FixtureRequest):
	"""
	Provides a Betamax cassette scoped to the test function
	which record and plays back interactions with the PubChem API.
	"""  # noqa: D400

	with Betamax(cached_requests) as vcr:
		# print(f"Using cassette {cassette_name!r}")
		vcr.use_cassette(request.node.name, record="none")

		yield cached_requests
