import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestMeeting:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('meeting', 'common')

    def test_validate_record(self):
        validate({
            'name': 'Name',
            'location': 'Location',
            'date': '2015',
            'number': '34',
            'full': 'Name 34 2015 Location'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '711__': {
                'a': 'Name',
                'c': 'Location',
                'd': '2015',
                'n': '34'
            }
        })
        assert record.get('meeting') == {
            'name': 'Name',
            'location': 'Location',
            'date': '2015',
            'number': '34',
            'full': 'Name 34 2015 Location'
        }

    def test_marc2marc(self):
        marc = {
            '711__': {
                'a': 'Name',
                'c': 'Location',
                'd': '2015',
                'n': '34'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'meeting': {
                'name': 'Name',
                'location': 'Location',
                'date': '2015',
                'number': '34',
                'full': 'Name 34 2015 Location'
            }
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/elements/1.1/contributor': [{
                '@value': 'Name 34 2015 Location'
            }]
        }]
