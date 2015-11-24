import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestInstitution:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('institution', 'common')

    def test_validate_record(self):
        validate({
            'name': 'HES-SO Valais',
            'code': 'HEVS_',
            'locality': 'Sion'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '919__': {
                'a': 'HES-SO Valais',
                'b': 'Sion'
            },
            '980__': {
                'b': 'HEVS_',
                'a': 'BOOK'
            }
        })
        assert record.get('institution') == {
            'name': 'HES-SO Valais',
            'code': 'HEVS_',
            'locality': 'Sion'
        }

    def test_marc2marc(self):
        marc = {
            '919__': {
                'a': 'HES-SO Valais',
                'b': 'Sion',
                'd': 'doc.support@rero.ch'
            },
            '980__': {
                'b': 'HEVS_',
                'a': 'BOOK'
            }
        }

        converted = marc2marc(marc)
        assert marc == converted

    def test_wrong_code_value(self):
        with pytest.raises(ValidationError):
            validate([{'code': 'TOTO'}], self.get_schema())
