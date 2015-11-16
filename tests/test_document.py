import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestDocument:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('document', 'common')

    def test_validate_record(self):
        validate([{
            'name': 'file_name.pdf',
            'mime': 'application/pdf',
            'size': 1014,
            'url': 'http://doc.rero.ch/record/file_name.pdf',
            'order': 1,
            'label': 'Main file'
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '8564_': [{
                'f': 'file_name.pdf',
                'q': 'application/pdf',
                's': '1014',
                'u': 'http://doc.rero.ch/record/file_name.pdf',
                'y': 'order:1',
                'z': 'Main file'
            }]
        })
        assert record == {
            'document': [{
                'name': 'file_name.pdf',
                'mime': 'application/pdf',
                'size': 1014,
                'url': 'http://doc.rero.ch/record/file_name.pdf',
                'order': 1,
                'label': 'Main file'
            }]
        }

    def test_marc2marc(self):
        marc = {
            '8564_': [{
                'f': 'file_name.pdf',
                'q': 'application/pdf',
                's': '1014',
                'u': 'http://doc.rero.ch/record/file_name.pdf',
                'y': 'order:1',
                'z': 'Main file'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_wrong_url_value(self):
        with pytest.raises(ValidationError):
            validate([{'url': 'http://rero.ch/files/test.pdf'}], self.get_schema())
