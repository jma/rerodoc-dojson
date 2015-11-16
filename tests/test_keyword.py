import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestKeyword:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('keyword', 'common')

    def test_validate_record(self):
        validate([{
            'lang': 'en',
            'content': ['keyword1', 'keyword2']
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '695__': [{
                '9': 'en',
                'a': 'keyword1 ; keyword2'
            }]
        })
        assert record == {
            'keyword': [{
                'lang': 'en',
                'content': ['keyword1', 'keyword2']
            }]
        }

    def test_marc2marc(self):
        marc = {
            '695__': [{
                '9': 'en',
                'a': 'keyword1 ; keyword2'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted
