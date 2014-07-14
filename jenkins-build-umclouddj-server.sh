#!/bin/bash

cd $WORKSPACE

#cd setup/android/

#run tests
#./unit-test-setup-android.sh emulate
coverage run --source='.' manage.py test
#python manage.py test
if [ "$?" != "0" ]; then
        echo "UMCloudDj UNIT TESTS FAIL: STOP!"
        exit 1
fi

echo "UMCloudDj UNIT TESTS PASS: CONTINUE"

#Build it.

sed -i.backup -e 's/^DEBUG=True/DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^DEBUG = True/DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^DEBUG =True/DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^DEBUG= True/DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py

sed -i.backup -e 's/^TEMPLATE_DEBUG=True/TEMPLATE_DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^TEMPLATE_DEBUG =True/TEMPLATE_DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^TEMPLATE_DEBUG = True/TEMPLATE_DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py
sed -i.backup -e 's/^TEMPLATE_DEBUG = True/TEMPLATE_DEBUG = False/' $WORKSPACE/UMCloudDj/settings.py

sed -i.backup -e 's/^SECRET_KEY/##/' $WORKSPACE/UMCloudDj/settings.py
echo "SECRET_KEY=\"ReplaceMe\"" >> $WORKSPACE/UMCloudDj/settings.py

cd $WORKSPACE
DATE=`date +%Y-%m-%d-%H-%M-%S`
mkdir build
rm -f build/*tar.gz
tar -zvcf build/UMCloudDj_${DATE}.tar.gz --exclude='build' *
coverage report
