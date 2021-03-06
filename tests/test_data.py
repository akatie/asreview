import urllib
from pathlib import Path

from pytest import mark

from asreview import ASReviewData
from asreview.datasets import DatasetManager
from asreview.search import fuzzy_find


def exists(url):
    return urllib.request.urlopen(url).getcode() == 200


@mark.parametrize("keywords,paper_id", [
    ("bronchogenic duplication cyst", 0),
    ("diagnositc accuracy microscopy female priority", 1),
    ("immunophenotiping", 4),
    ("Foregut report embryoogenesis", 4),
    ("Liu Adler", 0),
    ("Khoury cysts", 4),
    ("Isolated Edwards", 5),
    ("Kwintanilla-djeck Neck", 3),
    ("Cancer case computer contrast pancreatomy Yamada", 2),
])
def test_fuzzy_finder(keywords, paper_id):
    fp = Path("tests", "demo_data", "embase.csv")
    as_data = ASReviewData.from_file(fp)

    assert fuzzy_find(as_data, keywords)[0] == paper_id


@mark.parametrize("data_name", [
    "benchmark:van_de_Schoot_2017",
    "benchmark:Hall_2012",
    "benchmark:Cohen_2006_ACEInhibitors",
    "benchmark:Bos_2018",
])
def test_datasets(data_name):
    data = DatasetManager().find(data_name)
    assert exists(data.get())
