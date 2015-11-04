FROM python:2.7-slim

RUN mkdir /src
ADD rerodoc /src/rerodoc/rerodoc
ADD tests /src/rerodoc/tests
ADD scripts /src/rerodoc/scripts
COPY MANIFEST.in pytest.ini setup.py /src/rerodoc/

WORKDIR /src/rerodoc
RUN apt-get update -y && apt-get install -y gcc libxml2-dev libxslt1-dev python-dev lib32z1-dev
RUN pip install .
CMD py.test
