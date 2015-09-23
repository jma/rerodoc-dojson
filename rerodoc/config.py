#
## This file is part of INSPIRE.
## Copyright (C) 2014 CERN.
##
## INSPIRE is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## INSPIRE is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with INSPIRE; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#

"""
INSPIRE configuration
--------------------
Instance independent configuration (e.g. which extensions to load) is defined
in ``inspire.config'' while instance dependent configuration (e.g. database
host etc.) is defined in an optional ``inspire.instance_config'' which
can be installed by a separate package.

This config module is loaded by the Flask application factory via an entry
point specified in the setup.py::

    entry_points={
        'invenio.config': [
            "inspire = inspire.config"
        ]
    },
"""

from invenio.base.config import PACKAGES as _PACKAGES

PACKAGES = [
    #"rerodoc.base",
    u'rerodoc.dojson',
    #"rerodoc.modules.*",
] + _PACKAGES



# DoJSON configuration
RECORD_PROCESSORS = {
    'json': 'json.load',
    'marcxml': 'rerodoc.dojson.processors:convert_marcxml',
}



## Configuration related to Deposit module
#
#DEPOSIT_TYPES = [
#    'inspire.modules.deposit.workflows.literature.literature',
#    'inspire.modules.deposit.workflows.literature_simple.literature_simple',
#]
#DEPOSIT_DEFAULT_TYPE = "inspire.modules.deposit.workflows.literature:literature"
#
## facets ignored by auto-discovery service, they are not accessible in inspire
#PACKAGES_FACETS_EXCLUDE = [
#    'invenio.modules.search.facets.collection',
#]
#
## Task queue configuration
#
#CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
#CELERY_ACCEPT_CONTENT = ["msgpack"]
#BROKER_URL = "amqp://guest:guest@localhost:5672//"
#
## Site name configuration

CFG_SITE_LANG = u"fr"
CFG_SITE_LANGS = ['en', 'fr', 'de', 'it']

# CFG_SITE_NAME and main collection name should be the same for empty search
# to work
CFG_SITE_NAME = u"RERO DOC"

langs = {}
for lang in CFG_SITE_LANGS:
    langs[lang] = u"RERO DOC - Digital Library"
CFG_SITE_NAME_INTL = langs

CFG_EMAIL_BACKEND="flask.ext.email.backends.console.Mail"
CFG_BIBSCHED_PROCESS_USER="marietho"
CFG_DATABASE_NAME="rerodoc"
CFG_DATABASE_USER="rerodoc"
CFG_SITE_URL="http://0.0.0.0:4000"
CFG_SITE_SECURE_URL="http://0.0.0.0:4000"

DEBUG=True
ASSETS_DEBUG=True

# cause bad page reload
#LESS_RUN_IN_DEBUG=False

COLLECT_STORAGE="invenio.ext.collect.storage.link"
LESS_BIN = u'/Users/marietho/Devel/Virtualenvs/rerodoc/src/rerodoc/node_modules/.bin/lessc'
CLEANCSS_BIN = u'/Users/marietho/Devel/Virtualenvs/rerodoc/src/rerodoc/node_modules/.bin/cleancss'
REQUIREJS_BIN = u'/Users/marietho/Devel/Virtualenvs/rerodoc/src/rerodoc/node_modules/.bin/r.js'
UGLIFYJS_BIN = u'/Users/marietho/Devel/Virtualenvs/rerodoc/src/rerodoc/node_modules/.bin/uglifyjs'

from invenio.ext.es import SEARCH_RECORD_MAPPING
SEARCH_RECORD_MAPPING['mappings']['record']['properties'] = {
                "title": {
                    "type": "object",
                    "properties": {
                        "lang": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "subtitle": {
                            "type": "string",
                            "analyzer": "natural_text"
                        },
                        "title": {
                            "type": "string",
                            "analyzer": "natural_text"
                        }
                    }
                }
    }

# Rename blueprint prefixes

#BLUEPRINTS_URL_PREFIXES = {'webdeposit': '/submit'}

# Flask specific configuration - This prevents from getting "MySQL server
# has gone away" error

#SQLALCHEMY_POOL_RECYCLE = 700

# OAUTH configuration

#from invenio.modules.oauthclient.contrib import orcid
#orcid.REMOTE_SANDBOX_APP['params']['authorize_url'] = "https://sandbox.orcid.org/oauth/authorize#show_login"

# For production only, instance_config contains configuration of
# database credentials and other instance specific configuration
try:
    from rerodoc.instance_config import *
except ImportError:
    pass
