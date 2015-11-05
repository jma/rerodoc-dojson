import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestTitle:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('title', 'common')

    def test_validate_record(self):
        validate({
            'maintitle': 'Main Title',
            'subtitle': 'Subtitle',
            'lang': 'eng',
            'full': 'Main Title Subtitle'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '245__': {
                'a': 'Main Title',
                'b': "Subtitle",
                '9': 'eng'
            }
        })
        assert record == {
            'title': {
                'maintitle': 'Main Title',
                'subtitle': 'Subtitle',
                'lang': 'eng',
                'full': 'Main Title Subtitle'
            }
        }

    def test_marc2marc(self):
        marc = {
            '245__': {
                'a': 'Main Title',
                'b': "Subtitle",
                '9': 'eng'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'title': {
                'maintitle': 'Main Title',
                'subtitle': 'Subtitle',
                'lang': 'eng',
                'full': 'Main Title Subtitle'
            }
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/title': [{
                '@value': 'Main Title Subtitle',
                '@language': 'eng'
            }]
        }]
        assert converted == jsonld

    def test_wrong_value(self):
        with pytest.raises(ValidationError):
            validate({'title': {'lang': 'en'}}, self.get_schema())
