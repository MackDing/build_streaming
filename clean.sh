#! /bin/bash

find / -name '.git' \
-o -name '.gitignore' \
-o -name 'generateRsaKey.sh' \
-o -name 'oneKeyAuth.sh' \
-o -name 'oneKeyTest.sh' \
-o -name 'oneKeyTest_n.sh' \
-o -name 'ev_license' \
-o -name 'privateKey.pem' \
-o -name 'pubKey.pem' \
-o -name 'license.txt' \
-o -name 'r.txt' \
| xargs rm -rf

rm -rf /usr/local/ev_sdk/authorization/*
rm -rf /usr/local/ev_sdk/src
rm -rf /usr/local/ev_sdk/data/*

rm -rf /usr/local/ias/ias_data

rm -rf /usr/local/install
rm -rf /usr/local/*.gz
rm -rf /usr/local/*.zip

rm -rf /data/*

rm -rf /usr/local/clean.sh