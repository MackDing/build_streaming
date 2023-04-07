# /bin/bash
#  mkdir /usr/local/ev_sdk/result/${i%%.*};
version=`/usr/local/ev_sdk/bin/test-ji-api  2>&1| grep EV_SDK_VERSION`
echo $version
if [ -z "$version" ]
then
    echo "SDK版本：4.0"

    if [ "$1" = "video" ];
    then
        /usr/local/ev_sdk/bin/test-ji-api -f 1 -i /usr/local/ev_sdk/bin/dataset/$2 -o /usr/local/ev_sdk/bin/result/result_$2;
    else
        unzip /usr/local/ev_sdk/bin/dataset/$2 -d /usr/local/ev_sdk/bin/dataset;
        rm -rf /usr/local/ev_sdk/bin/dataset/$2;
        for i in `ls /usr/local/ev_sdk/bin/dataset/`; do /usr/local/ev_sdk/bin/test-ji-api -f 1 -i /usr/local/ev_sdk/bin/dataset/$i -o /usr/local/ev_sdk/bin/result/result_$i; done
        cd /usr/local/ev_sdk/bin/result && zip -r result_$2 ./*
    fi
else
    echo "SDK版本：3.0"
    cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/bin/ev_license && chmod +x /usr/local/ev_sdk/bin/ev_license && /usr/local/ev_sdk/bin/ev_license -r /usr/local/ev_sdk/bin/r.txt && /usr/local/ev_sdk/bin/ev_license -l /usr/local/ev_sdk/authorization/privateKey.pem /usr/local/ev_sdk/bin/r.txt /usr/local/ev_sdk/bin/license.txt
    if [ "$1" = "video" ];
    then
        /usr/local/ev_sdk/bin/test-ji-api -f 4 -i /usr/local/ev_sdk/bin/dataset/$2 -o /usr/local/ev_sdk/bin/result/result_$2;
    else
        unzip /usr/local/ev_sdk/bin/dataset/$2;
        rm -rf /usr/local/ev_sdk/bin/dataset/$2;
        for i in `ls /usr/local/ev_sdk/bin/dataset/`; do
            /usr/local/ev_sdk/bin/test-ji-api -f 1 -i /usr/local/ev_sdk/bin/dataset/$i -o /usr/local/ev_sdk/bin/result/result_$i;
        done
        zip /usr/local/ev_sdk/bin/result/result_$2 /usr/local/ev_sdk/bin/result/
    fi
fi
