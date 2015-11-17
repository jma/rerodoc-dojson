import pytest

from rerodoc.udc.udc import extract_rdf, update_udc, get_udc, UnsupportedError

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='need --runslow option to run'
)


class TestUDC:

    @slow
    def test_rdf_udc_import(self):
        udc = extract_rdf()
        assert udc.get('004', {}).get('uri') == 'http://udcdata.info/013566'

    @slow
    def test_update_udc(self):
        assert update_udc()

    def test_simple(self):
        assert get_udc('004').get('uri') == [
            'http://udcdata.info/013566'
        ]

    def test_multiple(self):
        assert get_udc('73/77').get('uri') == [
            'http://udcdata.info/065174',
            'http://udcdata.info/065213',
            'http://udcdata.info/065280',
            'http://udcdata.info/065294',
            'http://udcdata.info/065307'
        ]

    def test_parent(self):
        assert get_udc('614.253.5').get('uri') == [
            'http://udcdata.info/038191'
        ]

    def test_wrong_value(self):
        with pytest.raises(UnsupportedError):
            get_udc('foo')
