# Build image
# ./build.sh [version]

FROM python:3.5-slim

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

ARG AIRFLOW_HOME=/usr/local/airflow
ARG CODE_PATH=${AIRFLOW_HOME}/code

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

ARG BUILD_DEPS='python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git'

RUN set -ex \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $BUILD_DEPS \
        python3-pip \
        python3-requests \
        mysql-client \
        mysql-server \
        libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        vim \
        less \
        sudo \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install Cython \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install psutil \
    && pip install tox \
    && pip install celery[redis]==4.0.2

# Installing the postgresql-client needs some dirs that aren't included in the slim version
# https://github.com/dalibo/temboard/commit/ff98d6740ae11345658508b02052294d6cffd448
RUN mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get install -yqq --no-install-recommends postgresql-client

# Install debugging tools
RUN apt-get install -yqq --no-install-recommends \
        gdb \
        python3-dbg

ADD requirements.txt ${AIRFLOW_HOME}/requirements.txt
RUN pip install -r ${AIRFLOW_HOME}/requirements.txt

ENV PYTHONPATH=${CODE_PATH}
ENV PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
COPY airflow ${CODE_PATH}
RUN cd ${CODE_PATH} && export SLUGIFY_USES_TEXT_UNIDECODE=yes && pip install -e .[crypto,celery,postgres,hdfs,hive,jdbc,mysql,devel_ci]

# Thrift seems to cause issues so manually upgrading here
RUN pip install --upgrade thrift

RUN apt-get purge --auto-remove -yqq $BUILD_DEPS \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

# Should I just copy these over then create a volume when running compose???
VOLUME  ${AIRFLOW_HOME}/scripts
VOLUME  ${AIRFLOW_HOME}/config

# COPY entrypoint.sh /entrypoint.sh
# # This should be a volume so we don't need to rebuild the image every time this file changes
# COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_HOME}
RUN ln -s ${AIRFLOW_HOME}/config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
RUN ln -s ${AIRFLOW_HOME}/config/webserver_config.py ${AIRFLOW_HOME}/webserver_config.py

EXPOSE 8080 5555 8793

USER airflow
RUN usermod -aG sudo airflow

WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["${AIRFLOW_HOME}/scripts/entrypoint.sh"]

