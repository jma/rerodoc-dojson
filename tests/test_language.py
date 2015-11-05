import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestLanguage:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('language', 'common')

    def test_validate_record(self):
        validate('eng', self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '041__': {'a': 'eng'}
        })
        assert record.get('language') == 'eng'

    def test_marc2marc(self):
        marc = {'041__': {'a': 'eng'}}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'language': 'eng'
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/language': [{
                '@value': 'eng'
            }]
        }]
        assert converted == jsonld

    def test_wrong_value(self):
        with pytest.raises(ValidationError):
            validate('en', self.get_schema())
