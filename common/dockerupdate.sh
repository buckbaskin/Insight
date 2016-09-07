echo This script needs sudo to run docker build, docker push
sudo docker build -t buckbaskin/uwsgi-nginx:python3.5 .
sudo docker push buckbaskin/uwsgi-nginx

