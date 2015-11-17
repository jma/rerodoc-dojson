import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestDocumentType:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('document_type', 'common')

    def test_validate_record(self):
        validate({
            'main': 'book',
            'sub': 'book_proceed'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '980__': {'a': 'BOOK', 'f': 'BOOK_PROCEED'}
        })
        assert record.get('document_type') == {
            'main': 'book',
            'sub': 'book_proceed'
        }

    def test_marc2marc(self):
        marc = {
            '919__': {
                'a': 'HES-SO Valais',
                'b': 'Sion',
                'd': 'doc.support@rero.ch'
            },
            '980__': {
                'b': 'HEVS_',
                'a': 'BOOK',
                'f': 'BOOK_PROCEED'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_wrong_main_value(self):
        with pytest.raises(ValidationError):
            validate({'main': 'foo', 'sub': 'book_proceed'}, self.get_schema())

    def test_wrong_sub_value(self):
        with pytest.raises(ValidationError):
            validate({'main': 'book', 'sub': 'foo'}, self.get_schema())
