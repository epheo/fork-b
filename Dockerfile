FROM base/arch
MAINTAINER Thibaut Lapierre <root@epheo.eu>

RUN pacman -Sy --noconfirm
RUN pacman -S --noconfirm python2-pip git gcc

RUN git clone https://github.com/Epheo/fork-b.git
RUN pip2 install Flask Vincent

ENV HOME /fork-b

CMD 'git pull && python2 ./frontend/app.py'
