# docker build -t lilypond .
# docker run -v `pwd`:/work -it lilypond

FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install lilypond netpbm make locales-all
RUN apt install -y fonts-ipafont fonts-ipaexfont

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP.UTF-8
