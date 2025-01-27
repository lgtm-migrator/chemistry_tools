"""
test_pandas
~~~~~~~~~~~

Test optional pandas functionality.

"""

# 3rd party
import pandas  # type: ignore

# this package
from chemistry_tools.pubchem.compound import Compound, compounds_to_frame
from chemistry_tools.pubchem.properties import get_properties

#
# @pytest.mark.skip("TODO")
# @pytest.mark.flaky(reruns=5, reruns_delay=10)
# def test_compounds_dataframe():
# 	df = get_compounds('C20H41Br', 'formula', as_dataframe=True)
# 	assert df.ndim == 2
# 	assert df.index.names == ['CID']
# 	assert len(df.index) > 5
# 	columns = df.columns.values.tolist()
# 	assert 'atom_stereo_count' in columns
# 	assert 'atoms' in columns
# 	assert 'canonical_smiles' in columns
# 	assert 'exact_mass' in columns


def test_properties_dataframe(pubchem_cassette):
	df = get_properties("1,2,3,4", ["IsomericSMILES", "XLogP", "InChIKey"], "cid", as_dataframe=True)
	assert df.ndim == 2  # type: ignore
	assert df.index.names == ["CID"]  # type: ignore
	assert len(df.index) == 4  # type: ignore
	assert df.columns.values.tolist() == ["IsomericSMILES", "InChIKey", "XLogP"]  # type: ignore


def test_compound_series(pubchem_cassette):
	s = Compound.from_cid(241).to_series()
	assert isinstance(s, pandas.Series)


def test_compound_to_frame(pubchem_cassette):
	s = compounds_to_frame(Compound.from_cid(241))
	assert isinstance(s, pandas.DataFrame)
