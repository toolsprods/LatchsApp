#!/bin/bash

if [ -z "$1" ]; then
 echo -e "\nUsage: $0 pair_token \n"
 exit 0
fi

ApplicationId="APP_ID_HERE"
SecretKey="SECRET_KEY_HERE"

Server="https://latch.elevenpaths.com"
URL="/api/1.0/pair/$1"

requestSignature+="GET\n"
date=`date -u '+%Y-%m-%d %H:%M:%S'`
requestSignature+="$date\n\n$URL"
signed=`echo -en "$requestSignature" | openssl dgst -sha1 -hmac "$SecretKey" -binary`
b64signed=`echo -n "$signed"|base64`

auth_header="Authorization:11PATHS $ApplicationId $b64signed"
date_header="X-11Paths-Date: $date"

response=`curl -q -s -N --header "$auth_header" --header "$date_header" "$Server$URL"`

echo $response
