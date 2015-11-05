FROM python:2.7-slim

# copy sources
RUN mkdir /src
ADD rerodoc /src/rerodoc/rerodoc
ADD tests /src/rerodoc/tests
ADD scripts /src/rerodoc/scripts
COPY tox.ini MANIFEST.in pytest.ini setup.py /src/rerodoc/

WORKDIR /src/rerodoc

# install dependencies (gcc is needed by lxml)
RUN apt-get update -y && apt-get install -y gcc libxml2-dev libxslt1-dev python-dev lib32z1-dev

# install the package
RUN pip install .

RUN pip install tox

# command to run in the container
CMD py.test
