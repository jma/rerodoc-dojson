import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestExternalLink:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('external_link', 'common')

    def test_validate_record(self):
        validate([{
            'url': 'http://doc.rero.ch',
            'datetime': '2007-11-25 23:47:43',
            'label': 'Home Page'
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '8564_': [{
                'u': 'http://doc.rero.ch',
                'y': '2007-11-25 23:47:43',
                'z': 'Home Page'
            }]
        })
        assert record == {
            'external_link': [{
                'url': 'http://doc.rero.ch',
                'datetime': '2007-11-25 23:47:43',
                'label': 'Home Page'
            }]
        }

    def test_marc2marc(self):
        marc = {
            '8564_': [{
                'u': 'http://doc.rero.ch',
                'y': '2007-11-25 23:47:43',
                'z': 'Home Page'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted
