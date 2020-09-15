# docker run -v `pwd`:/work -it lilypond

FROM ubuntu:16.04

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP.UTF-8

RUN apt-get update
RUN apt-get -y install lilypond netpbm make
RUN apt install -y fonts-ipafont fonts-ipaexfont