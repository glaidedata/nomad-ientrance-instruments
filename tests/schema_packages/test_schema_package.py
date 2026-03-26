import os

from nomad.client.processing import parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    # The parse function automatically builds the archive data
    entry_archive = parse(test_file)[0]

    # 1. Assert Core Fields
    assert entry_archive.data.name == 'Test Instrument'
    assert entry_archive.data.lab_id == '999'
    assert entry_archive.data.manufacturer == 'Test Corp'

    # 2. Assert Techniques Subsection
    assert len(entry_archive.data.techniques) == 1
    assert entry_archive.data.techniques[0].name == 'Scanning Electron Microscopy'

    # 3. Assert Managers Subsection
    assert len(entry_archive.data.managers) == 1
    assert entry_archive.data.managers[0].firstname == 'John'
    assert entry_archive.data.managers[0].lastname == 'Doe'
