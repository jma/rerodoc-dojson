import pytest
from conftest import marc2record, marc2marc, record2jsonld


class TestLanguage:

    def test_validate_record(self):
        from rerodoc.dojson.utils import get_schema
        from jsonschema import validate
        validate('eng', get_schema('language', 'book'))

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
        from rerodoc.dojson.utils import get_schema
        from jsonschema import validate, ValidationError
        with pytest.raises(ValidationError):
            validate('en', get_schema('language', 'book'))
