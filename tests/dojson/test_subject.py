import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestSubject:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('subject', 'common')

    def test_validate_record(self):
        validate([{
            'vocabulary': 'rero',
            'tag': '650_7',
            'content': 'Inventaires'
        }], self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '600__': [{
                '2': 'rero',
                '9': '650_7',
                'a': 'Inventaires'
            }]
        })
        assert record == {
            'subject': [{
                'vocabulary': 'rero',
                'tag': '650_7',
                'content': 'Inventaires'
            }]
        }

    def test_mesh_from_marc(self):
        record = marc2record({
            '600__': [{
                '9': '650_2',
                'a': 'Inventaires'
            }]
        })
        assert record == {
            'subject': [{
                'vocabulary': 'mesh',
                'tag': '650_2',
                'content': 'Inventaires'
            }]
        }

    def test_mesh_marc2marc(self):
        marc = {
            '600__': [{
                '9': '650_2',
                'a': 'Inventaires'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_lcsh_from_marc(self):
        record = marc2record({
            '600__': [{
                '9': '650__',
                'a': 'Inventaires'
            }]
        })
        assert record == {
            'subject': [{
                'vocabulary': 'lcsh',
                'tag': '650__',
                'content': 'Inventaires'
            }]
        }

    def test_lcsh_marc2marc(self):
        marc = {
            '600__': [{
                '9': '650__',
                'a': 'Inventaires'
            }]
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_wrong_vocabulary_value(self):
        with pytest.raises(ValidationError):
            validate([{'vocabulary': 'invalid'}], self.get_schema())

    def test_wrong_tag_value(self):
        with pytest.raises(ValidationError):
            validate([{'tag': '245__'}], self.get_schema())

    def test_wrong_tag_indicator_value(self):
        with pytest.raises(ValidationError):
            validate([{'tag': '65_0_'}], self.get_schema())
