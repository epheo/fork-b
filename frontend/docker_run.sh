
# docker run -d -p 80:80 -v .:/haproxy-override dockerfile/haproxy

docker build -t iojs-app

docker run -v ${PWD}:/usr/src/app -w /usr/src/app -p 5000:8080 --it --rm iojs iojs charts.js
