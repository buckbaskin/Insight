FROM buckbaskin/uwsgi-nginx:python3.5

MAINTAINER William Baskin <mobile.wbaskin@gmail.com>

RUN pip install flask

COPY ./requirements.txt /home/requirements.txt

RUN pip install -r /home/requirements.txt

COPY nginx.conf /etc/nginx/conf.d/

COPY ./app /app

