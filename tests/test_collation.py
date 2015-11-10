import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestCollation:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('collation', 'common')

    def test_validate_record(self):
        validate({
            'pages': '100 p.',
            'other': 'ill.',
            'dimension': '25 x 30 cm',
            'full': '100 p. ill. 25 x 30 cm'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '300__': {
                'a': '100 p.',
                'b': 'ill.',
                'c': '25 x 30 cm'
            }
        })
        assert record.get('collation') == {
            'pages': '100 p.',
            'other': 'ill.',
            'dimension': '25 x 30 cm',
            'full': '100 p. ill. 25 x 30 cm'
        }

    def test_marc2marc(self):
        marc = {
            '300__': {
                'a': '100 p.',
                'b': 'ill.',
                'c': '25 x 30 cm'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'collation': {
                'pages': '100 p.',
                'other': 'ill.',
                'dimension': '25 x 30 cm',
                'full': '100 p. ill. 25 x 30 cm'
            }
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/elements/1.1/format': [{
                '@value': '100 p. ill. 25 x 30 cm'
            }]
        }]
