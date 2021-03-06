# -*- coding: utf-8 -*-
import pytest
from conftest import marc2record, marc2marc, record2jsonld
from jsonschema import validate, ValidationError


class TestPublication:

    # helpers
    def get_schema(self):
        from rerodoc.dojson.utils import get_schema
        return get_schema('publication', 'common')

    def test_validate_record(self):
        validate({
            'location': 'Location',
            'publisher': 'Publisher',
            'date': '2015-',
            'print_location': 'Print Location',
            'printer': 'Printer',
            'full': 'Location Publisher 2015- Print Location Printer'
        }, self.get_schema())

    def test_from_marc(self):
        record = marc2record({
            '260__': {
                'a': 'Location',
                'b': 'Publisher',
                'c': '2015-',
                'e': 'Print Location',
                'f': 'Printer'
            }
        })
        assert record.get('publication') == {
            'location': 'Location',
            'publisher': 'Publisher',
            'date': '2015-',
            'print_location': 'Print Location',
            'printer': 'Printer',
            'full': 'Location Publisher 2015- Print Location Printer'
        }

    def test_marc2marc(self):
        marc = {
            '260__': {
                'a': 'Location',
                'b': 'Publisher',
                'c': '2015-',
                'e': 'Print Location',
                'f': 'Printer'
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_empty_260_marc2marc(self):
        marc = {
            "260__": {
                "a": "A Lausanne :",
                "c": "1744",
                "b": "chez Bousquet & Compagnie,",
                "e": "Lausanne"
            },
            "035__": {
                "a": "R004127217"
            },
            "990__": {
                "a": "20061123145722-ML"
            }
        }
        converted = marc2marc(marc)
        assert marc == converted

    def test_jsonld(self, book_context):
        record = {
            'recid': '1234',
            'publication': {
                'location': 'Location',
                'publisher': 'Publisher',
                'date': '2015-',
                'print_location': 'Print Location',
                'printer': 'Printer',
                'full': 'Location Publisher 2015- Print Location Printer'
            }
        }
        converted = record2jsonld(record, book_context)
        assert converted == [{
            '@id': 'http://doc.rero.ch/record/1234',
            'http://rdaregistry.info/Elements/u/publicationStatement': [{
                '@value': 'Location Publisher 2015- Print Location Printer'
            }]
        }]
