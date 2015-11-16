import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestOtherEdtion:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('other_edition', 'common')

    def test_validate_record(self):
        validate({
            'type': 'Published Version',
            'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '775__': {
                'g': 'Published Version',
                'o': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
            }
        })
        assert record == {
            'other_edition': {
                'type': 'Published Version',
                'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
            }
        }

    def test_marc2marc(self):
        marc = {
            '775__': {
                'g': 'Published Version',
                'o': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_wrong_url_value(self):
        with pytest.raises(ValidationError):
            validate({'url': 'bla'}, self.get_schema())

    def test_validate_secure_record(self):
        validate({
            'type': 'Published Version',
            'url': 'https://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }, self.get_schema())
