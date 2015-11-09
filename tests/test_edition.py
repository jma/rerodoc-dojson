import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestEdition:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('edition', 'common')

    def test_validate_record(self):
        validate({
            'name': 'Name',
            'remainder': 'Remainder',
            'full': 'Name Remainder'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '250__': {
                'a': 'Name',
                'b': 'Remainder'
            }
        })
        assert record == {
            'edition': {
                'name': 'Name',
                'remainder': 'Remainder',
                'full': 'Name Remainder'
            }
        }

    def test_marc2marc(self):
        marc = {
            '250__': {
                'a': 'Name',
                'b': 'Remainder'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'edition': {
                'name': 'Name',
                'remainder': 'Remainder',
                'full': 'Name Remainder'
            }
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/ontology/bibo/edition': [{
                '@value': 'Name Remainder'
            }]
        }]
