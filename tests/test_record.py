import pytest


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
        graph = Graph().parse(data=json.dumps(compacted, indent=2), format="json-ld")
        print(graph.serialize(format="turtle"))
