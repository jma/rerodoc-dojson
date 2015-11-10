import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestNPages:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('n_pages', 'common')

    def test_validate_record(self):
        validate(100, self.get_schema())

    def test_simple_from_marc(self):
        record = marc2record({
            '300__': {
                'a': '100'
            }
        })
        assert record.get('n_pages') == 100

    def test_simple_fr_from_marc(self):
        record = marc2record({
            '300__': {'a': '25 p.'}
        })
        assert record.get("n_pages") == 25

    def test_simple_ger_from_marc(self):
        record = marc2record({
            '300__': {'a': '230 s.'}
        })
        assert record.get("n_pages") == 230

    def test_sheet_from_marc(self):
        record = marc2record({
            '300__': {'a': '230 f.'}
        })
        assert record.get("n_pages") == 230

    def test_bad_pages(self):
        record = marc2record({
            '300__': {'a': 'A25 j. fjklad'}
        })
        assert record.get("n_pages") == None
