#!/bin/bash
current=""
while true; do
	latest=`ec2metadata --public-ipv4`
	echo "public-ipv4=$latest"
	if [ "$current" == "$latest" ]
	then
		echo "ip not changed"
	else
		echo "ip has changed - updating"
		current=$latest
		echo url="https://www.duckdns.org/update?domains=crbvc&token=3caead8d-9872-4534-ab13-814ca5f4128c&ip=" | curl -k -o ~/duck.log -K -
	fi
	sleep 5m
done