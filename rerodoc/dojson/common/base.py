# -*- coding: utf-8 -*-

"""MARC 21 model definition."""

from dojson import utils
from ..book.model import book, book2marc
from .. import utils as myutils
import re


@book.over('recid', '^001')
def control_number(self, key, value):
    """Record Identifier."""
    return value[0]


@book2marc.over('001', 'recid')
def control_number2marc(self, key, value):
    """Record Identifier."""
    return [value]


@book.over('rero_id', '^035__')
def rero_id(self, key, value):
    """Language Code."""
    return "http://data.rero.ch/01-" + value.get('a')


@book2marc.over('035__', 'rero_id')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.replace("http://data.rero.ch/01-", "")
    }


@book.over('language', '^041[10_].')
def language(self, key, value):
    """Language Code."""
    return value.get('a')


@book2marc.over('041__', 'language')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': value
    }


@book.over('udc', '^080__')
def udc(self, key, value):
    """Language Code."""
    from rerodoc.udc.udc import get_udc
    code = value.get('a')
    values = get_udc(code)
    values['code'] = code
    return values


@book2marc.over('080__', 'udc')
def udc2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.get('code')
    }


@book.over('authors', '^[17]00__')
# @utils.filter_values
def authors(self, key, value):
    """Record Document Type."""
    value = utils.force_list(value)

    def get_value(value):
        full = myutils.concatenate(value, ['a', 'd'])
        #if value.get("e"):
        #    full = full + " (" + value.get("e") + ")"

        to_return = {
            "name": value.get("a"),
            "date": value.get("d"),
            "role": value.get("e"),
            "full": full,
            "affiliation": value.get("u")
        }
        return dict((k, v) for k, v in to_return.items() if v)
    authors = self.get('authors', [])

    if key.startswith('100'):
        authors.insert(0, get_value(value[0]))
    else:
        for val in value:
            authors.append(get_value(val))
    return authors


@book2marc.over('100__', 'authors')
# @utils.filter_values
def authors2marc(self, key, value):
    """Main Entry-Personal Name."""
    value = utils.force_list(value)

    def get_value(value):
        to_return = {
            'a': value.get('name'),
            'e': value.get('role'),
            'd': value.get('date'),
            'u': value.get('affiliation')
        }
        return dict((k, v) for k, v in to_return.items() if v)

    if len(value) > 1:
        self["700__"] = []
    for author in value[1:]:
        self["700__"].append(get_value(author))

    return get_value(value[0])


@book.over('title', '^245__')
@utils.filter_values
def title(self, key, value):
    """Other title Statement."""
    return {
        'maintitle': value.get('a'),
        'subtitle': value.get('b'),
        'full': myutils.concatenate(value, ['a', 'b']),
        'lang': value.get('9')
    }


@book2marc.over('245__', 'title')
@utils.filter_values
def title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('maintitle'),
        'b': value.get('subtitle'),
        '9': value.get('lang')
    }


@book.over('other_title', '^246__')
@utils.filter_values
def other_title(self, key, value):
    """Other title Statement."""
    return {
        'maintitle': value.get('a'),
        'full': value.get('a'),
        'lang': value.get('9')
    }


@book2marc.over('246__', 'other_title')
@utils.filter_values
def other_title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('maintitle'),
        '9': value.get('lang')
    }


@book.over('edition', '^250__')
@utils.filter_values
def edition(self, key, value):
    """Edition Statement."""
    return {
        'name': value.get('a'),
        'full': myutils.concatenate(value, ['a', 'b']),
        'remainder': value.get('b')
    }


@book2marc.over('250__', 'edition')
@utils.filter_values
def edition2marc(self, key, value):
    """Edition Statement."""
    return {
        'a': value.get('name'),
        'b': value.get('remainder')
    }


@book.over('publication_date', '^260__')
@utils.ignore_value
def publication_date(self, key, value):
    """Title Statement."""
    raw_date = value.get('c')
    if not raw_date:
        return None

    res = re.findall(r"(\d{4})", raw_date)
    res = [int(v) for v in res]
    if not res:
        return None

    if len(res) == 1:
        if re.search(r'\d{4}-', raw_date):
            return {
                'full': '%d-' % res[0],
                'from': res[0]
            }
        else:
            return {
                'full': '%d' % res[0],
                'from': res[0],
                'to': res[0]
            }
    res.sort()
    return {
        'full': '%d-%d' % (res[0], res[-1]),
        'from': res[0],
        'to': res[-1]
    }


@book.over('publication', '^260__')
@utils.filter_values
def publication(self, key, value):
    """Publication Statement."""
    return {
        'location': value.get('a'),
        'publisher': value.get('b'),
        'date': value.get('c'),
        'print_location': value.get('e'),
        'printer': value.get('f'),
        'full': myutils.concatenate(value, ['a', 'b', 'c', 'e', 'f'])
    }


@book2marc.over('260__', 'publication')
@utils.filter_values
def publication2marc(self, key, value):
    """Edition Statement."""
    return {
        'a': value.get('location'),
        'b': value.get('publisher'),
        'c': value.get('date'),
        'e': value.get('print_location'),
        'f': value.get('printer')
    }


@book.over('n_pages', '^300__')
@utils.ignore_value
def number_of_pages(self, key, value):
    """Number of pages Statement."""
    raw_pages = value.get('a')
    if not raw_pages:
        return None

    n_pages = re.findall(r'(\d+)\s*(?:p|s|f)', raw_pages, re.IGNORECASE)
    if n_pages:
        return int(n_pages[0])
    else:
        n_pages = re.findall(r'^(\d+)$', raw_pages)
        if n_pages:
            return int(n_pages[0])
    return None


@book.over('dimension', '^300__')
@utils.ignore_value
def dimension(self, key, value):
    """Document dimension in cm."""
    raw_dimension = value.get('c')
    if not raw_dimension:
        return None

    dimension = re.findall(r'(\d+)\s*x\s*(\d+)\s*cm', raw_dimension, re.IGNORECASE)

    if dimension:
        return {
            "width": int(dimension[0][0]),
            "height": int(dimension[0][1])
        }
    else:
        dimension = re.findall(r'(\d+)\s*cm', raw_dimension, re.IGNORECASE)

        if dimension:
            return {
                "width": int(dimension[0])
            }
    return None


@book.over('collation', '^300__')
@utils.filter_values
def publication(self, key, value):
    """Collation Statement."""
    return {
        'pages': value.get('a'),
        'other': value.get('b'),
        'dimension': value.get('c'),
        'full': myutils.concatenate(value, ['a', 'b', 'c'])
    }


@book2marc.over('300__', 'collation')
@utils.filter_values
def publication2marc(self, key, value):
    """Collation Statement."""
    return {
        'a': value.get('pages'),
        'b': value.get('other'),
        'c': value.get('dimension')
    }


@book.over('series', '^490__')
@utils.filter_values
def series(self, key, value):
    """Series Statement."""
    return {
        'name': value.get('a'),
        'volume': value.get('v'),
        'full': myutils.concatenate(value, ['a', 'v'], " ; ")
    }


@book2marc.over('490__', 'series')
@utils.filter_values
def series2marc(self, key, value):
    """Collation Statement."""
    return {
        'a': value.get('name'),
        'v': value.get('volume')
    }


@book.over('note', '^500__')
def note(self, key, value):
    """Note Statement."""
    return value.get('a')


@book2marc.over('500__', 'note')
def note2marc(self, key, value):
    """Note Statement."""
    return {
        'a': value
    }


@book.over('content_note', '^505__')
def content_note(self, key, value):
    """Content Note Statement."""
    return value.get('a')


@book2marc.over('505__', 'content_note')
def content_note2marc(self, key, value):
    """Content Note Statement."""
    return {
        'a': value
    }


@book.over('summary', '^520__')
@utils.for_each_value
def summary(self, key, value):
    """Summary Statement."""
    return {
        'content': value.get('a'),
        'lang': value.get('9')
    }


@book2marc.over('520__', 'summary')
@utils.for_each_value
def series2marc(self, key, value):
    """Summary Statement."""
    return {
        'a': value.get('content'),
        '9': value.get('lang')
    }


@book.over('reproduction', '^533__')
@utils.filter_values
def reproduction(self, key, value):
    """Reproduction Statement."""
    return {
        'type': value.get('a'),
        'location': value.get('b'),
        'agency': value.get('c'),
        'date': value.get('d')
    }


@book2marc.over('533__', 'reproduction')
@utils.filter_values
def reproduction2marc(self, key, value):
    """Summary Statement."""
    return {
        'a': value.get('type'),
        'b': value.get('location'),
        'c': value.get('agency'),
        'd': value.get('date')
    }


@book.over('subject', '^600__')
@utils.for_each_value
def subject(self, key, value):
    """Subject Statement."""
    return {
        'vocabulary': value.get('2'),
        'tag': value.get('9'),
        'content': value.get('a')
    }


@book2marc.over('600__', 'subject')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    return {
        '2': value.get('vocabulary'),
        '9': value.get('tag'),
        'a': value.get('content')
    }


@book.over('keyword', '^695__')
@utils.for_each_value
def keyword(self, key, value):
    """Keyword Statement."""
    return {
        'lang': value.get('9'),
        'content': [v.strip() for v in value.get('a').split(";")]
    }


@book2marc.over('695__', 'keyword')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    return {
        '9': value.get('lang'),
        'a': " ; ".join(value.get('content'))
    }


@book.over('corporate', '^710__')
@utils.for_each_value
def corporate(self, key, value):
    return value.get('a')


@book2marc.over('710__', 'corporate')
@utils.for_each_value
def corporate2marc(self, key, value):
    """Meeting Statement."""
    return {
        "a": value
    }


@book.over('meeting', '^711__')
@utils.filter_values
def meeting(self, key, value):
    return {
        'name': value.get('a'),
        'location': value.get('c'),
        'date': value.get('d'),
        'number': value.get('n'),
        'full': myutils.concatenate(value, ['a', 'n', 'd', 'c'])
    }


@book2marc.over('711__', 'meeting')
@utils.filter_values
def meeting2marc(self, key, value):
    """Meeting Statement."""
    return {
        "a": value.get("name"),
        "c": value.get("location"),
        "d": value.get("date"),
        "n": value.get("number")
    }


@book.over('other_edition', '^775__')
@utils.filter_values
def other_edition(self, key, value):
    return {
        'type': value.get('g'),
        'url': value.get('o')
    }


@book2marc.over('775__', 'other_edition')
@utils.filter_values
def other_edition2marc(self, key, value):
    """Other Edition Statement."""
    return {
        "g": value.get("type"),
        "o": value.get("url")
    }


@book.over('media_type', '^980__')
def media_type(self, key, value):
    """Record Document Type."""
    return "http://rdvocab.info/termList/RDAMediaType/1003"


@book.over('type', '^980__')
def document_type(self, key, value):
    """Record Document Type."""
    doc_type = value.get("a")
    return ['bibrec', doc_type.lower(), 'text']


@book2marc.over('980__', 'type')
def document_type2marc(self, key, value):
    """Record Document Type."""
    return {
        "a": value[1].upper()
    }
