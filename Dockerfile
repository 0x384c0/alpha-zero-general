FROM      gw000/keras:2.1.4-py3-tf-cpu
MAINTAINER 0x384c0 [https://github.com/0x384c0/] <0x384c0@gmail.com>

RUN pip3 --no-cache-dir install flask==1.0.2

ARG CACHEBUST=1

RUN mkdir /app \
&& cd /app \
&& git clone https://github.com/0x384c0/alpha-zero-general.git \
&& cd /app/alpha-zero-general \
&& mkdir temp \
&& chmod -R +x scripts

WORKDIR /app/alpha-zero-general

ADD https://github.com/0x384c0/alpha-zero-general/releases/download/1.0/best.pth.tar temp

ENTRYPOINT scripts/docker_entrypoint.sh