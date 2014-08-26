if [ $# -eq 0 ]; then
    echo "No arguments provided"
    echo "Usage: .sh <Super username> <password> <wordpress pass> <um pass> <secret key>"
    echo "Ex:    .sh adminusername adminpassword worddpass umtestpass secretkey_10212wdsda><?:<>!@%*%$"
    exit 1
fi

if [ $# -ne 5 ]; then
    echo "You need to give 5 arguments"
    echo "Usage: .sh <Super username> <password> <wordpress pass> <um pass> <secret key>"
    echo "Ex:    .sh adminusername adminpassword worddpass umtestpass secretkey_10212wdsda><?:<>!@%*%$"
    exit 1
fi


SUPERUSERNAME=${1}
SUPERPASSWORD=${2}
WORDPRESSPASS=${3}
UMPASS=${4}
SECRET_KEY=${5}

DATE=`date +%Y-%m-%d-%H-%M-%S`
echo "Starting installation of UMCDjCloud."
echo "Sorting and installing dependencies.."
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install apache2
sudo apt-get -y install python
sudo apt-get -y install python-pip python-virtualenv
sudo apt-get -y install tree
sudo apt-get -y install git
sudo apt-get -f install
sudo apt-get -y install sqlite3
sudo apt-get -y install build-essential

sudo pip install Django
sudo pip install requests
sudo pip install coverage
sudo pip install Image

git clone ssh://varunasingh@git.code.sf.net/p/ustadmobil/code-umclouddjango UMCloudDj

> UMCloudDj/UMCloudDj/wordpresscred.txt
> UMCloudDj/UMCloudDj/media/gruntConfig/umpassword.txt
echo "${WORDPRESSPASS}" > UMCloudDj/UMCloudDj/wordpresscred.txt		#Soon to be depreciated. Was used for authenticting wordpress users. 
echo "${UMPASS}" > UMCloudDj/UMCloudDj/media/gruntConfig/umpassword.txt #Soon to be depreciated . Was used for testing course pass/fail when sent to server

cd UMCloudDj

cp UMCloudDj/settings.py.edit UMCloudDj/settings.py

#Need to update the secret key
sed -i.bak -e 's/^SECRET_KEY/##/' UMCloudDj/settings.py
echo "SECRET_KEY=\"${SECRET_KEY}\"" >> UMCloudDj/settings.py

#After getting latest version, we use this to create super user and assign database mappings:
#Creates a super user and syncs models and databases
python manage.py syncdb --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${SUPERUSERNAME}', 'info@ustadmobile.com', '${SUPERPASSWORD}')" | python manage.py shell

#load fixtures
python manage.py loaddata uploadeXe/fixtures/initial-model-data.json
DATE2=`date +%Y-%m-%d`

echo "from uploadeXe.models import User_Roles; User_Roles.objects.create(name='build',user_userid_id=1,role_roleid_id=1,add_date='${DATE2}')" | python manage.py shell
echo "from organisation.models import User_Organisations; User_Organisations.objects.create(add_date='${DATE2}',user_userid_id=1,organisation_organisationid_id=1)" | python manage.py shell

cd UMCloudDj/media/
mkdir eXeExport
mkdir eXeUpload
mkdir test
mkdir eXeTestElp
mkdir eXeTestExport


