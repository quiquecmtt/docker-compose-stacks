!# /bin/sh

rootdir=$PWD

cd $rootdir/networking && docker-compose up -d
cd $rootdir/management && docker-compose up -d
cd $rootdir/file-sharing && docker-compose up -d
cd $rootdir/databases && docker-compose up -d
cd $rootdir

