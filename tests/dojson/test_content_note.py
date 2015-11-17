import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestContentNote:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('content_note', 'common')

    def test_validate_record(self):
        validate(['Note line 1\n Line 2'], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '505__': [{'a': 'Note Line 1\n Line 2'}]
        })
        assert record.get('content_note') == ['Note Line 1\n Line 2']

    def test_marc2marc(self):
        marc = {'505__': [{'a': 'Note line 1\n Line 2'}]}
        converted = marc2marc(marc)
        assert marc == converted
