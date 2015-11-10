"""MARC 21 model definition."""

from ..model import book, book2marc
from dojson import utils
import re

ISBN10_REGEX = re.compile(r'^[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,7}-[0-9,X]{1}$')
ISBN13_REGEX = re.compile(r'^978[0-9]{9}[0-9]{1}$')


@book.over('isbn10', '^020..')
@utils.ignore_value
def isbn10(self, key, value):
    """Other Standard Identifier."""
    isbn = value.get('a')
    if ISBN10_REGEX.match(isbn):
        return value.get('a')
    return None


@book2marc.over('020__', 'isbn10')
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
    if ISBN13_REGEX.match(isbn) == 13:
        return value.get('a')
    return None


@book2marc.over('020__', 'isbn13')
def isbn132marc(self, key, value):
    """Other Standard Identifier."""
    return {
        'a': value
    }
