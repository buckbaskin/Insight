echo This script needs sudo to run docker build, docker push
sudo docker build -t buckbaskin/insight-main:v1 .
sudo docker push buckbaskin/insight-main

