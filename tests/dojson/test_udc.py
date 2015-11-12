import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestUDC:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('udc', 'common')

    def test_validate_record(self):
        validate({
            'code': '004',
            'en': 'Computer science',
            'fr': 'Informatique',
            'de': 'Informatik',
            'it': "Informatique",
            'uri': ['http://udcdata.info/013566']
        }, self.get_schema())

    def test_validate_range_record(self):
        validate({
            'code': '93/94',
        }, self.get_schema())

    def test_validate_3_levels_record(self):
        validate({
            'code': '614.253.1',
        }, self.get_schema())

    def test_validate_quote_record(self):
        validate({
            'code': '81`28',
        }, self.get_schema())

    def test_validate_wrong_quote_value(self):
        with pytest.raises(ValidationError):
            validate({'code': "81'28"}, self.get_schema())

    def test_wrong_3_levels_value(self):
        with pytest.raises(ValidationError):
            validate({'code': "614.253.544"}, self.get_schema())

    def test_validate_2_levels_record(self):
        validate({
            'code': '615.84',
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '080__': {'a': '004'}
        })
        assert record.get('udc') == {
            'code': '004',
            'en': 'Computer science',
            'fr': 'Informatique',
            'de': 'Informatik',
            'it': "Informatique",
            'uri': ['http://udcdata.info/013566']
        }

    def test_marc2marc(self):
        marc = {'080__': {'a': '004'}}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'udc': {
                'code': '004',
                'en': 'Computer science',
                'fr': 'Informatique',
                'de': 'Informatik',
                'it': "Informatique",
                'uri': ['http://udcdata.info/013566']
            }
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/subject': [{
                '@id': 'http://udcdata.info/013566'
            }]
        }]
        assert converted == jsonld
