"""MARC 21 model definition."""

from ..model import book, book2marc
from dojson import utils


@book.over('isbn10', '^020..')
@utils.ignore_value
def isbn10(self, key, value):
    """Other Standard Identifier."""
    isbn = value.get('a')
    if len(isbn) == 10:
        return value.get('a')
    return None


@book2marc.over('020', 'isbn10')
def isbn102marc(self, key, value):
    """Other Standard Identifier."""
    return {
        'a': value
    }


@book.over('isbn13', '^020..')
@utils.ignore_value
def isbn13(self, key, value):
    """Other Standard Identifier."""
    isbn = value.get('a')
    if len(isbn) == 13:
        return value.get('a')
    return None


@book2marc.over('020', 'isbn13')
def isbn132marc(self, key, value):
    """Other Standard Identifier."""
    return {
        'a': value
    }
