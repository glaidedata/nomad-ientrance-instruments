import os
from nomad.client.processing import parse
from nomad.processing.data import normalize_all

def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    # Assert that our custom schema parsed the ID correctly
    assert entry_archive.data.fablims_id == 999
    assert entry_archive.data.manufacturer == 'Test Corp'