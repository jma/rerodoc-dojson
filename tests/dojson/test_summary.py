import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestSummary:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('summary', 'common')

    def test_validate_record(self):
        validate([{
            'lang': 'en',
            'content': 'Summary Line 1\n Line2'
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '520__': [{
                'a': 'Summary Line 1\n Line2',
                '9': 'en'
            }]
        })
        assert record == {
            'summary': [{
                'lang': 'en',
                'content': 'Summary Line 1\n Line2'
            }]
        }

    def test_marc2marc(self):
        marc = {
            '520__': [{
                'a': 'Summary Line 1\n Line2',
                '9': 'en'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted
