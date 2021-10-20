docker rm -f $(docker ps -a -q)
docker build -t checker:etna .
docker run -v /var/run/docker.sock:/var/run/docker.sock -d -p 8080:8080 checker:etna
