
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

@book.over('type', '^980__')
def document_type(self, key, value):
    """Record Document Type."""
    return value.get("a").lower()

@book2marc.over('980', 'type')
def document_type2marc(self, key, value):
    """Record Document Type."""
    return {
        "a": value
    }
