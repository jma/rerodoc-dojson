from setuptools import setup

from distutils.core import setup, Command
# you can also import from setuptools

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call(["py.test", 'tests'])
        raise SystemExit(errno)


setup(
    name="RERO DOC",
    version="0.1.dev0",
    url="http://doc.rero.ch/",
    author="Johnny Mariethoz - RERO",
    author_email="doc.support@rero.ch",
    description="RERO DOC - Digital Library",
    install_requires=[
        "dojson>=0.1.1",
        "PyLD>=0.6.8",
        "rdflib-jsonld>=0.3",
        "jsonschema>=2.5.1",
        "pytest>=2.8.0",
        "pytest-cache>=1.0",
        "pytest-cov>=2.1.0",
        "pytest-pep8>=1.0.6"
    ],
    cmdclass = {'test': PyTest},
    entry_points={
        "invenio.config": ["rerodoc = rerodoc.config"]
    }
)
