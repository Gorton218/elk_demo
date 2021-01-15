#!/bin/bash
echo stopping logstash ...
docker-compose --project-directory /vagrant stop logstash
sleep 5
echo "   done"
for NAME in logstash deployments; do
  echo recreating $NAME
  curl -X DELETE 127.0.0.1:9200/$NAME*
  PAYLOAD="{\"aliases\": {\"$NAME\": {\"is_write_index\": true}}}"
  curl -X PUT -H "Content-Type: application/json" -d "$PAYLOAD" localhost:9200/%3C${NAME}-%7Bnow%2Fd%7D-000001%3E
  echo "   done"
done
echo starting logstash
docker-compose --project-directory /vagrant up -d logstash
echo "   done"
echo recreation finished
