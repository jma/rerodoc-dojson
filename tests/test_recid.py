import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestRecId:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('recid', 'common')

    def test_validate_record(self):
        validate('1234', self.get_schema())
    
    def test_from_marc(self):
        record = marc2record({
            '001': ['1234']
        })
        assert record.get('recid') == '1234'

    def test_marc2marc(self):
        marc = {'001': ['1234']}
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'rero_id': 'http://data.rero.ch/01-R1234'
        }
        converted = record2jsonld(record, book_context)
        assert converted[0].get('@id') == 'http://doc.rero.ch/record/1234'
