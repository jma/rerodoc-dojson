import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestISBN13:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('isbn13', 'book')

    def test_validate_record(self):
        validate('9782882250209',
                 self.get_schema())

    def test_invalid_record(self):
        with pytest.raises(ValidationError):
            validate('2-88147-009-2',
                     self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '020__': {
                'a': '9782882250209'
            }
        })
        assert record.get('isbn13') == '9782882250209'

    def test_marc2marc(self):
        marc = {'020__': {'a': '9782882250209'}}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'isbn13': '9782882250209'
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/ontology/bibo/isbn13': [{
                '@value': '9782882250209'
            }]
        }]
