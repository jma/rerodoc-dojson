# -*- coding: utf-8 -*-

import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestRestrictedAccess:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('access_restriction', 'common')

    def test_validate_record(self):
        validate({
            'message': u'Accès réservé aux institutions membres de RERO',
            'code': 'Restricted access'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '506__': {
                'a': u'Accès réservé aux institutions membres de RERO',
                'f': 'Restricted access',
            }
        })
        assert record.get('access_restriction') == {
            'message': u'Accès réservé aux institutions membres de RERO',
            'code': 'Restricted access'
        }

    def test_marc2marc(self):
        marc = {
            '506__': {
                'a': u'Accès réservé aux institutions membres de RERO',
                'f': 'Restricted access',
            }
        }
        converted = marc2marc(marc)
        assert marc == converted
