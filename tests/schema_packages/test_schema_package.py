import os

from nomad.client.processing import parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    # The parse function automatically builds the archive data
    entry_archive = parse(test_file)[0]

    # Assert that our custom schema parsed the ID correctly
    assert entry_archive.data.fablims_id == 999  # noqa PLR2004
    assert entry_archive.data.manufacturer == 'Test Corp'
