import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestReproduction:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('reproduction', 'common')

    def test_validate_record(self):
        validate({
            'type': 'Type',
            'location': 'Location',
            'agency': 'Agency',
            'date': '2015.'
            #'year': 2015
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '533__': {
                'a': 'Type',
                'b': 'Location',
                'c': 'Agency',
                'd': '2015.'
            }
        })
        assert record.get('reproduction') == {
            'type': 'Type',
            'location': 'Location',
            'agency': 'Agency',
            'date': '2015.'
        }

    def test_marc2marc(self):
        marc = {
            '533__': {
                'a': 'Type',
                'b': 'Location',
                'c': 'Agency',
                'd': '2015.'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted
