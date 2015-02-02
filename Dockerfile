FROM base/arch
MAINTAINER Thibaut Lapierre <root@epheo.eu>


RUN git clone https://github.com/Epheo/fork-b.git
RUN pip install Flask
RUN pip install Vincent
