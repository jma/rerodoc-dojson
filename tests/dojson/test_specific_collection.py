import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestSpecificCollection:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('specific_collection', 'common')

    def test_validate_record(self):
        validate([{
            'code': 'CODE',
            'name': 'Collection Name'
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '982__': [{
                'a': 'CODE',
                'b': 'Collection Name',
            }]
        })
        assert record.get('specific_collection') == [{
            'code': 'CODE',
            'name': 'Collection Name'
        }]

    def test_marc2marc(self):
        marc = {
            '982__': [{
                'a': 'CODE',
                'b': 'Collection Name',
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted
