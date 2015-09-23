import pytest

class TestRecord:

    def test_rec_id_marc21_from_xml(self, book_schema, simple_book_record):
      from jsonschema import validate
      from dojson.contrib.marc21.utils import create_record
      from rerodoc.dojson.book import book
      blob = create_record(simple_book_record)
      data = book.do(blob)
      validate(data, book_schema)
