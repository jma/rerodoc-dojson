import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestOtherTitle:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('title', 'common')

    def test_validate_record(self):
        validate({
            'maintitle': 'Other Title',
            'lang': 'eng',
            'full': 'Other Title'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '246__': {
                'a': 'Other Title',
                '9': 'eng'
            }
        })
        assert record == {
            'other_title': {
                'maintitle': 'Other Title',
                'lang': 'eng',
                'full': 'Other Title'
            }
        }

    def test_marc2marc(self):
        marc = {
            '246__': {
                'a': 'Other Title',
                '9': 'eng'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'other_title': {
                'maintitle': 'Other Title',
                'lang': 'eng',
                'full': 'Other Title'
            }
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/alternative': [{
                '@value': 'Other Title',
                '@language': 'eng'
            }]
        }]
        assert converted == jsonld

    def test_wrong_value(self):
        with pytest.raises(ValidationError):
            validate({'other_title': {'lang': 'en'}}, self.get_schema())
