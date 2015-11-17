import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestType:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('type', 'common')

    def test_validate_record(self):
        validate(['bibrec', 'book', 'text'], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '980__': {'a': 'BOOK'}
        })
        assert record.get('type') == ['bibrec', 'book', 'text']

    def test_marc2marc(self):
        marc = {
            '919__': {
                'a': 'HES-SO Valais',
                'b': 'Sion',
                'd': 'doc.support@rero.ch'
            },
            '980__': {
                'b': 'HEVS_',
                'a': 'BOOK'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'type': ['bibrec', 'book', 'text']
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            '@type': [
                'http://purl.org/dc/terms/BibliographicResource',
                'http://purl.org/ontology/bibo/Book',
                'http://purl.org/dc/dcmitype/Text',
            ]
        }]
        assert converted == jsonld

    def test_wrong_book_only_value(self):
        with pytest.raises(ValidationError):
            validate(['book'], self.get_schema())
