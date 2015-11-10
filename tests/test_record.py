import pytest


class TestConfig:

    def test_get_wrong_schema(self):
        from rerodoc.dojson.utils import get_schema
        assert get_schema("not_exists") == None

    def test_get_wrong_context(self):
        from rerodoc.dojson.utils import get_context
        assert get_context("not_exists") == None
