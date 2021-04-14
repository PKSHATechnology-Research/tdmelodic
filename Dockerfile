FROM ubuntu:20.04
# To enable GPU, use other base images such as
# nvidia/cuda:10.0-devel-ubuntu16.04

# apt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc g++ cmake \
        unzip xz-utils \
    	libblas3 libblas-dev \
        mecab libmecab-dev swig \
        locales \
        fonts-ipafont fonts-ipaexfont fonts-takao-pgothic fonts-takao-mincho \
        python3-dev python3-pip python3-setuptools python3-tk && \
    rm -rf /var/lib/apt/lists/*
# The fonts are used only for plotting images (optional). The line can be removed.

# language=Japanese
RUN locale-gen ja_JP.UTF-8 \
    && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc

# Python
ARG PYTHON_VERSION=3.7
RUN echo "alias python='python3'" >> ~/.bash_aliases

# workspace
ARG workspace=/root/workspace
ENV PYTHONPATH $workspace:$workspace/tdmelodic
RUN mkdir -p $workspace

# Install UniDic
# Download this file in advance. The downloaded file will be reused later.
ARG UNIDIC='unidic-mecab_kana-accent-2.1.2_src'
ADD ${UNIDIC}.zip $workspace
WORKDIR $workspace
RUN unzip ${UNIDIC}.zip && \
    cd $workspace/${UNIDIC} && \
    ./configure && make && make install && cd - && \
    rm ${UNIDIC}.zip && rm -rf ${UNIDIC}

# pip
ENV pip='python3 -m pip'
ADD requirements.txt $workspace
WORKDIR $workspace
RUN $pip install --upgrade pip && \
    $pip install --upgrade setuptools && \
    $pip install wheel && \
    $pip install -r requirements.txt
