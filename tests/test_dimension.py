import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestDimension:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('dimension', 'common')

    def test_validate_record(self):
        validate({
            'width': 150,
            'height': 200
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '300__': {
                'c': '150 x 200 cm'
            }
        })
        assert record.get('dimension') == {
            'width': 150,
            'height': 200
        }

    def test_simple_from_marc(self):
        record = marc2record({
            '300__': {'c': '25 cm'}
        })
        assert record.get("dimension") == {"width": 25}
