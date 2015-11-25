# -*- coding: utf-8 -*-

"""MARC 21 model definition."""

from dojson import utils
from ..book.model import book, book2marc
from ..audio.model import audio, audio2marc
from .. import utils as myutils
from ..utils import ln2lang, lang2ln
import re


@book.over('recid', '^001')
@audio.over('recid', '^001')
def control_number(self, key, value):
    """Record Identifier."""
    return value[0]


@book2marc.over('001', 'recid')
@audio2marc.over('001', 'recid')
def control_number2marc(self, key, value):
    """Record Identifier."""
    return [value]


@book.over('rero_id', '^035__')
@audio.over('rero_id', '^035__')
def rero_id(self, key, value):
    """Language Code."""
    return "http://data.rero.ch/01-" + value.get('a')


@book2marc.over('035__', 'rero_id')
@audio2marc.over('035__', 'rero_id')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.replace("http://data.rero.ch/01-", "")
    }


@book.over('language', '^041[10_].')
@audio.over('language', '^041[10_].')
def language(self, key, value):
    """Language Code."""
    return lang2ln(value.get('a'))


@book2marc.over('041__', 'language')
@audio2marc.over('041__', 'language')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': ln2lang(value)
    }


@book.over('udc', '^080__')
@audio.over('udc', '^080__')
@utils.ignore_value
def udc(self, key, value):
    """Language Code."""
    from rerodoc.udc.udc import get_udc
    code = value.get('a')
    values = get_udc(code)
    if values:
        values['code'] = code
    return values


@book2marc.over('080__', 'udc')
@audio2marc.over('080__', 'udc')
@utils.ignore_value
def udc2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.get('code')
    }


@book.over('authors', '^[17]00__')
@audio.over('authors', '^[17]00__')
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
@audio2marc.over('100__', 'authors')
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
@audio.over('title', '^245__')
@utils.filter_values
def title(self, key, value):
    """Other title Statement."""
    return {
        'maintitle': value.get('a'),
        'subtitle': value.get('b'),
        'full': myutils.concatenate(value, ['a', 'b']),
        'lang': lang2ln(value.get('9'))
    }


@book2marc.over('245__', 'title')
@audio2marc.over('245__', 'title')
@utils.filter_values
def title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('maintitle'),
        'b': value.get('subtitle'),
        '9': ln2lang(value.get('lang'))
    }


@book.over('other_title', '^246__')
@audio.over('other_title', '^246__')
@utils.filter_values
def other_title(self, key, value):
    """Other title Statement."""
    return {
        'maintitle': value.get('a'),
        'full': value.get('a'),
        'lang': lang2ln(value.get('9'))
    }


@book2marc.over('246__', 'other_title')
@audio2marc.over('246__', 'other_title')
@utils.filter_values
def other_title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('maintitle'),
        '9': ln2lang(value.get('lang'))
    }


@book.over('edition', '^250__')
@audio.over('edition', '^250__')
@utils.filter_values
def edition(self, key, value):
    """Edition Statement."""
    return {
        'name': value.get('a'),
        'full': myutils.concatenate(value, ['a', 'b']),
        'remainder': value.get('b')
    }


@book2marc.over('250__', 'edition')
@audio2marc.over('250__', 'edition')
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


@book2marc.over('260__', '^publication$')
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
@audio.over('series', '^490__')
@utils.filter_values
def series(self, key, value):
    """Series Statement."""
    return {
        'name': value.get('a'),
        'volume': value.get('v'),
        'full': myutils.concatenate(value, ['a', 'v'], " ; ")
    }


@book2marc.over('490__', 'series')
@audio2marc.over('490__', 'series')
@utils.filter_values
def series2marc(self, key, value):
    """Collation Statement."""
    return {
        'a': value.get('name'),
        'v': value.get('volume')
    }


@book.over('note', '^500__')
@audio.over('note', '^500__')
def note(self, key, value):
    """Note Statement."""
    return value.get('a')


@book2marc.over('500__', 'note')
@audio2marc.over('500__', 'note')
def note2marc(self, key, value):
    """Note Statement."""
    return {
        'a': value
    }


@book.over('content_note', '^505__')
@audio.over('content_note', '^505__')
@utils.for_each_value
def content_note(self, key, value):
    """Content Note Statement."""
    return value.get('a')


@book2marc.over('505__', 'content_note')
@audio2marc.over('505__', 'content_note')
@utils.for_each_value
def content_note2marc(self, key, value):
    """Content Note Statement."""
    return {
        'a': value
    }


@book.over('access_restriction', '^506__')
@audio.over('access_restriction', '^506__')
@utils.filter_values
def access_restriction(self, key, value):
    """Content Note Statement."""
    to_return = {}
    return {
        'message': value.get('a'),
        'code': value.get('f')
    }


@book2marc.over('506__', 'access_restriction')
@audio2marc.over('506__', 'access_restriction')
@utils.filter_values
def access_restriction2marc(self, key, value):
    """Content Note Statement."""
    return {
        'a': value.get('message'),
        'f': value.get('code')
    }


@book.over('summary', '^520__')
@audio.over('summary', '^520__')
@utils.for_each_value
def summary(self, key, value):
    """Summary Statement."""
    return {
        'content': value.get('a'),
        'lang': lang2ln(value.get('9'))
    }


@book2marc.over('520__', 'summary')
@audio2marc.over('520__', 'summary')
@utils.for_each_value
def series2marc(self, key, value):
    """Summary Statement."""
    return {
        'a': value.get('content'),
        '9': ln2lang(value.get('lang'))
    }


@book.over('reproduction', '^533__')
@audio.over('reproduction', '^533__')
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
@audio2marc.over('533__', 'reproduction')
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
@audio.over('subject', '^600__')
@utils.for_each_value
def subject(self, key, value):
    """Subject Statement."""
    to_return = {
        'tag': value.get('9'),
        'content': value.get('a')
    }
    vocabulary = value.get('2')
    if not vocabulary:
        ind = value.get('9')[-1]
        if ind == '2':
            vocabulary = 'mesh'
        elif ind == '_':
            vocabulary = 'lcsh'
    if vocabulary:
        to_return['vocabulary'] = vocabulary

    return to_return


@book2marc.over('600__', 'subject')
@audio2marc.over('600__', 'subject')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    to_return = {
        '9': value.get('tag'),
        'a': value.get('content')
    }
    vocabulary = value.get('vocabulary')
    if vocabulary and vocabulary not in ['mesh', 'lcsh']:
        to_return['2'] = vocabulary
    return to_return


@book.over('keyword', '^695__')
@audio.over('keyword', '^695__')
@utils.for_each_value
def keyword(self, key, value):
    """Keyword Statement."""
    return {
        'lang': lang2ln(value.get('9')),
        'content': [v.strip() for v in value.get('a').split(";")]
    }


@book2marc.over('695__', 'keyword')
@audio2marc.over('695__', 'keyword')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    return {
        '9': ln2lang(value.get('lang')),
        'a': " ; ".join(value.get('content'))
    }


@book.over('corporate', '^710__')
@audio.over('corporate', '^710__')
@utils.for_each_value
def corporate(self, key, value):
    return value.get('a')


@book2marc.over('710__', 'corporate')
@audio2marc.over('710__', 'corporate')
@utils.for_each_value
def corporate2marc(self, key, value):
    """Meeting Statement."""
    return {
        "a": value
    }


@book.over('meeting', '^711__')
@audio.over('meeting', '^711__')
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
@audio2marc.over('711__', 'meeting')
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
@audio.over('other_edition', '^775__')
@utils.filter_values
def other_edition(self, key, value):
    return {
        'type': value.get('g'),
        'url': value.get('o')
    }


@book2marc.over('775__', 'other_edition')
@audio2marc.over('775__', 'other_edition')
@utils.filter_values
def other_edition2marc(self, key, value):
    """Other Edition Statement."""
    return {
        "g": value.get("type"),
        "o": value.get("url")
    }


@book.over('document', '^8564_')
@audio.over('document', '^8564_')
@utils.ignore_value
def document(self, key, value):
    value = utils.force_list(value)
    document = self.get('document', [])

    def get_value(value):
        return {
            'name': value.get('f'),
            'mime': value.get('q'),
            'size': int(value.get('s')),
            'url': value.get('u'),
            'order': int(value.get('y').replace('order:', '')),
            'label': value.get('z')
        }
    for val in value:
        if val.get('q'):
            document.append(get_value(val))
    return document or None


@book2marc.over('8564_', '(^document$|external_link)')
@audio2marc.over('8564_', '(^document$|external_link)')
def document2marc(self, key, value):
    """Document Statement."""
    value = utils.force_list(value)
    f8564 = self.get('8564_', [])
    links = []
    document = []
    if key.startswith('external_link'):
        def get_value(value):
            return {
                'u': value.get('url'),
                'y': value.get('datetime'),
                'z': value.get('label')
            }
        for val in value:
            links.append(get_value(val))
        return links + f8564
    else:
        def get_value(value):
            return {
                'f': value.get('name'),
                'q': value.get('mime'),
                's': str(value.get('size')),
                'u': value.get('url'),
                'y': "order:%s" % value.get('order'),
                'z': value.get('label')
            }
        for val in value:
            document.append(get_value(val))
        return f8564 + document
    return f8564


@book.over('external_link', '^8564_')
@audio.over('external_link', '^8564_')
@utils.ignore_value
def external_link(self, key, value):
    value = utils.force_list(value)
    links = self.get('external_link', [])

    def get_value(value):
        return {
            'url': value.get('u'),
            'datetime': value.get('y'),
            'label': value.get('z')
        }
    for val in value:
        if not val.get('q'):
            links.append(get_value(val))
    return links or None


@book.over('institution', '^(919|980)__')
@audio.over('institution', '^(919|980)__')
@utils.filter_values
def institution(self, key, value):
    institution = self.get('institution', {})
    if key.startswith('919'):
        institution.update({
            'name': value.get('a'),
            'locality': value.get('b')
        })
    if key.startswith('980'):
        institution.update({
            'code': value.get('b')
        })
    return institution


@book2marc.over('919__', 'institution')
@audio2marc.over('919__', 'institution')
@utils.filter_values
def institution2marc(self, key, value):
    """Institution Statement."""
    return {
        'a': value.get('name'),
        'b': value.get('locality'),
        'd': 'doc.support@rero.ch'
    }


@book.over('media_type', '^980__')
@audio.over('media_type', '^980__')
def media_type(self, key, value):
    """Record Document Type."""
    return "http://rdvocab.info/termList/RDAMediaType/1003"


@book.over('type', '^980__')
@audio.over('type', '^980__')
def type(self, key, value):
    """Record Document Type."""
    doc_type = value.get('a')
    return ['bibrec', doc_type.lower(), 'text']


@book.over('document_type', '^980__')
@audio.over('document_type', '^980__')
@utils.filter_values
def document_type(self, key, value):
    """Record Document Type."""
    doc_type = value.get('a').lower()
    doc_subtype = value.get('f')
    if doc_subtype:
        doc_subtype = doc_subtype.lower()
    return {
        'main': doc_type,
        'sub': doc_subtype
    }


@book2marc.over('980__', '(document_type|institution)')
@audio2marc.over('980__', '(document_type|institution)')
@utils.filter_values
def type_institution2marc(self, key, value):
    """Record Document Type and Institution."""
    marc = self.get('980__', {})
    if key.startswith('document_type'):
        doc_subtype = value.get('sub')
        if doc_subtype:
            doc_subtype = doc_subtype.upper()
        marc.update({
            'a': value.get('main').upper(),
            'f': doc_subtype
        })
    elif key.startswith('institution'):
        marc.update({
            'b': value.get('code')
        })
    return marc


@book.over('specific_collection', '^982__')
@audio.over('specific_collection', '^982__')
@utils.for_each_value
@utils.filter_values
def specific_collection(self, key, value):
    """Specific Collection Statement."""
    return {
        'code': value.get('a'),
        'name': value.get('b')
    }


@book2marc.over('982__', 'specific_collection')
@audio2marc.over('982__', 'specific_collection')
@utils.for_each_value
@utils.filter_values
def series2marc(self, key, value):
    """Specific Collection Statement."""
    return {
        'a': value.get('code'),
        'b': value.get('name')
    }


@book.over('submission_number', '^990__')
@audio.over('submission_number', '^990__')
def submission_number(self, key, value):
    """Submission Number Statement."""
    return value.get('a')


@book2marc.over('990__', 'submission_number')
@audio2marc.over('990__', 'submission_number')
def submission_number2marc(self, key, value):
    """Submission Number Statement."""
    return {
        'a': value
    }
