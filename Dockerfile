FROM ubuntu:14.04

MAINTAINER John Paul Newman, johnpaul.newman@gmail.com

RUN echo "deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main" > /etc/apt/sources.list.d/deadsnakes.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DB82666C

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    software-properties-common \
    python-software-properties \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    mercurial \
    pkg-config \
    python3.6 \
    python3.6-dev \
    sudo \
    ssh \
    && apt-get autoremove \
    && apt-get clean

# Install RethinkDB.
RUN \
  echo "deb http://download.rethinkdb.com/apt `lsb_release -cs` main" > /etc/apt/sources.list.d/rethinkdb.list && \
  wget -O- http://download.rethinkdb.com/apt/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -y rethinkdb python-pip && \
  rm -rf /var/lib/apt/lists/*

# Define mountable directories.
VOLUME ["/rethinkdb_data"]

VOLUME ["/app/upload"]

ADD https://raw.githubusercontent.com/pypa/pip/5d927de5cdc7c05b1afbdd78ae0d1b127c04d9d0/contrib/get-pip.py /root/get-pip.py

RUN python3.6 /root/get-pip.py
RUN pip3.6 install --upgrade pip

RUN pip3.6 install -U "setuptools==18.4"
RUN pip3.6 install -U "pip==7.1.2"
RUN pip3.6 install -U "virtualenv==13.1.2"

COPY . /app
WORKDIR /app

RUN pip3.6 install -r requirements.txt

# Define default command.
CMD ["rethinkdb", "--bind", "all", "--daemon"]

# CMD ["/usr/bin/python3.6", "run.py", "migrate"]
# CMD ["/usr/bin/python3.6", "run.py", "runserver", "--host=0.0.0.0", "--port=5000"]

EXPOSE 8080
EXPOSE 28015
EXPOSE 29015

EXPOSE 5000
