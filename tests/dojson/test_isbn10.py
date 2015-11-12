import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestISBN10:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('isbn10', 'book')

    def test_validate_record(self):
        validate('2-88147-009-2',
                 self.get_schema())

    def test_invalid_record(self):
        with pytest.raises(ValidationError):
            validate('9782882250209',
                     self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '020__': {
                'a': '2-88147-009-2'
            }
        })
        assert record.get('isbn10') == '2-88147-009-2'

    def test_marc2marc(self):
        marc = {'020__': {'a': '2-88147-009-2'}}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'isbn10': '2-88147-009-2'
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/ontology/bibo/isbn10': [{
                '@value': '2-88147-009-2'
            }]
        }]
