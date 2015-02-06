FROM base/arch
MAINTAINER Thibaut Lapierre <root@epheo.eu>

RUN pacman -Sy --noconfirm
RUN pacman -S --noconfirm python2-pip git gcc

RUN git clone https://github.com/Epheo/fork-b.git
RUN pip2 install Flask Vincent

RUN git --git-dir=/fork-b/.git --work-tree=/fork-b/ checkout doc

CMD git --git-dir=/fork-b/.git --work-tree=/fork-b/ pull && python2 /fork-b/frontend/app.py
