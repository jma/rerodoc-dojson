import pytest


class TestConfig:

    def test_get_wrong_schema(self):
        from rerodoc.dojson.utils import get_schema
        assert get_schema("not_exists") == None

    def test_get_wrong_context(self):
        from rerodoc.dojson.utils import get_context
        assert get_context("not_exists") == None


class TestRecord:

    def test_validate_record(self, book_schema, simple_book_record):
        from jsonschema import validate
        validate(simple_book_record, book_schema)

    def test_json_ld(self, book_context, book_schema, simple_book_record):
        from pyld import jsonld
        import json
        import rdflib_jsonld
        from rdflib import Graph
        import copy
        rec = copy.deepcopy(simple_book_record)
        rec.update(book_context)
        compacted = jsonld.compact(rec, book_context)
        expanded = jsonld.expand(compacted)
        graph = Graph().parse(data=json.dumps(expanded, indent=2), format="json-ld")
        #print("JSONL: %s" % graph.serialize(format="json-ld"))

    # def test_marc_xml_export(self, simple_book_record):
    #     from rerodoc.dojson.book import book2marc
    #     print book2marc.do(simple_book_record)

    def test_book_simple_date(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '260__': {'c': '2015'}
        })
        assert data.get("publication_date") == {'to': 2015, 'full': '2015', 'from': 2015}

    def test_book_from_date(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '260__': {'c': '2015-'}
        })
        assert data.get("publication_date") == {'full': '2015-', 'from': 2015}

    def test_book_full_date(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '260__': {'c': '2015 bla 2013 bla 2001'}
        })
        assert data.get("publication_date") == {'to': 2015, 'full': '2001-2015', 'from': 2001}

    def test_book_invalid_date(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '260__': {'c': '209 jfkad afje788'}
        })
        assert data.get("publication_date", None) == None

    def test_book_simple_n_pages_fr(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'a': '25 p.'}
        })
        assert data.get("n_pages") == 25

    def test_book_n_pages_ger(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'a': '230 s.'}
        })
        assert data.get("n_pages") == 230

    def test_book_n_pages_sheet(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'a': '230 f.'}
        })
        assert data.get("n_pages") == 230

    def test_book_simple_n_pages(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'a': '25'}
        })
        assert data.get("n_pages") == 25

    def test_book_simple_bad_pages(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'a': 'A25 j. fjklad'}
        })
        assert data.get("n_pages") == None

    def test_book_simple_dimension(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'c': '25 cm'}
        })
        assert data.get("dimension") == {"width": 25}

    def test_book_full_dimension(self):
        from rerodoc.dojson.book import book
        data = book.do({
            '300__': {'c': '25 x 30 cm'}
        })
        assert data.get("dimension") == {"width": 25, "height": 30}
