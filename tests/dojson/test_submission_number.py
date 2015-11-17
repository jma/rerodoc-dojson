import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestSubmissionNumber:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('submission_number', 'common')

    def test_validate_record(self):
        validate('20151116123706-NI', self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '990__': {'a': '20151116123706-NI'}
        })
        assert record.get('submission_number') == '20151116123706-NI'

    def test_marc2marc(self):
        marc = {'990__': {'a': '20151116123706-NI'}}
        converted = marc2marc(marc)
        assert marc == converted
