import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestSeries:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('series', 'common')

    def test_validate_record(self):
        validate({
            'name': 'Name',
            'volume': '3',
            'full': 'Name ; 3'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '490__': {
                'a': 'Name',
                'v': '3'
            }
        })
        assert record.get('series') == {
            'name': 'Name',
            'volume': '3',
            'full': 'Name ; 3'
        }

    def test_marc2marc(self):
        marc = {
            '490__': {
                'a': 'Name',
                'v': '3'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'series': {
                'name': 'Name',
                'volume': '3',
                'full': 'Name ; 3'
            }
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/bibliographicCitation': [{
                '@value': 'Name ; 3'
            }]
        }]
