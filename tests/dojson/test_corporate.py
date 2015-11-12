import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestCorporate:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('corporate', 'common')

    def test_validate_record(self):
        validate(["Corporate name"], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '710__': {
                'a': 'Corporate name'
            }
        })
        assert record == {
            'corporate': ['Corporate name']
        }

    def test_marc2marc(self):
        marc = {
            '710__': [{
                'a': 'Corporate name',
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'corporate': ['Corporate name', 'Corporate name2']
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/elements/1.1/contributor': [{
                '@value': 'Corporate name'
            }, {
                '@value': 'Corporate name2'
            }]
        }]
