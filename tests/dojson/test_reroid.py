import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestREROID:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('rero_id', 'common')

    def test_validate_record(self):
        validate('http://data.rero.ch/01-R1234', self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '035__': {'a': 'R1234'}
        })
        assert record.get('rero_id') == 'http://data.rero.ch/01-R1234'

    def test_marc2marc(self):
        marc = {'035__': {'a': 'R1234'}}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'rero_id': 'http://data.rero.ch/01-R1234'
        }
        converted = record2jsonld(record, book_context)
        jsonld = [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://purl.org/dc/terms/hasFormat': [{
                '@id': 'http://data.rero.ch/01-R1234'
            }]
        }]
        assert converted == jsonld

    def test_wrong_value(self):
        with pytest.raises(ValidationError):
            validate('R1234', self.get_schema())
