# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""MARC 21 model definition."""

from dojson import utils
from ..book.model import book, book2marc


@book.over('title', '^245[10_][0_]')
@utils.filter_values
def title(self, key, value):
    """Title Statement."""
    full = [value.get('a')]
    if value.get('b'):
        full.append(value.get('b'))
    return {
        'maintitle': value.get('a'),
        'subtitle': value.get('b'),
        'full': ": ".join(full),
        'lang': value.get('9')
    }


@book2marc.over('245', 'title')
@utils.for_each_value
@utils.filter_values
def title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('maintitle'),
        'b': value.get('subtitle'),
        '9': value.get('lang'),
    }


@book.over('recid', '^001')
def control_number(self, key, value):
    """Record Identifier."""
    return value[0]


@book2marc.over('001', 'control_number')
def control_number2marc(self, key, value):
    """Record Identifier."""
    return value


@book.over('rero_id', '^035__')
def rero_id(self, key, value):
    """Language Code."""
    return "http://data.rero.ch/01-" + value.get('a')


@book2marc.over('035', 'rero_id')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.replace("http://data.rero.ch/01-", "")
    }


@book.over('language', '^041[10_].')
def language(self, key, value):
    """Language Code."""
    return value.get('a')


@book2marc.over('041', 'language')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': value
    }


@book.over('media_type', '^980__')
def media_type(self, key, value):
    """Record Document Type."""
    return "http://rdvocab.info/termList/RDAMediaType/1003"


@book.over('type', '^980__')
def document_type(self, key, value):
    """Record Document Type."""
    return ["bibrec", value.get("a").lower()]


@book2marc.over('980', 'type')
def document_type2marc(self, key, value):
    """Record Document Type."""
    return {
        "a": value[1].upper()
    }


@book.over('authors', '^[17]00__')
# @utils.filter_values
def authors(self, key, value):
    """Record Document Type."""
    value = utils.force_list(value)

    def get_value(value):
        full = value.get("a")
        if value.get("d"):
            full = full + " " + value.get("d")
        if value.get("e"):
            full = full + " (" + value.get("e") + ")"

        to_return = {
            "name": value.get("a"),
            "date": value.get("d"),
            "role": value.get("e"),
            "full": full,
            "affiliation": value.get("u")
        }
        return {k: v for k, v in to_return.items() if v}
    authors = self.get('authors', [])

    if key.startswith('100'):
        authors.insert(0, get_value(value[0]))
    else:
        for val in value:
            authors.append(get_value(val))
    return authors


@book2marc.over('100', 'authors')
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
        return {k: v for k, v in to_return.items() if v}

    if len(value) > 1:
        self["700"] = []
    for author in value[1:]:
        self["700"].append(get_value(author))

    return get_value(value[0])
