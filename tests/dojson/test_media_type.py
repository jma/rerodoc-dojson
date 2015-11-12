import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestMediaType:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('media_type', 'common')

    def test_validate_record(self):
        validate('http://rdvocab.info/termList/RDAMediaType/1003',
                 self.get_schema())

    def test_simple_from_marc(self):
        record = marc2record({
            '980__': {
                'a': 'BOOK'
            }
        })
        assert record.get('media_type') == 'http://rdvocab.info/termList/RDAMediaType/1003'

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'media_type': 'http://rdvocab.info/termList/RDAMediaType/1003'
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://rdaregistry.info/Elements/u/mediaType': [{
                '@id': 'http://rdvocab.info/termList/RDAMediaType/1003'
            }]
        }]
