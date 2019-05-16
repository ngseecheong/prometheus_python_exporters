FROM python:stretch
RUN apt-get install -y gcc
ADD . /code
WORKDIR /code
RUN tar -xf ibm_mq.tar.gz -C /opt
ENV LD_LIBRARY_PATH="/opt/mqm/lib64/compat:/opt/mqm/lib/compat"
RUN pip3 install -r requirements.txt

