#! /bin/sh

rootdir=$PWD

cd $rootdir/databases && docker-compose down
cd $rootdir/file-sharing && docker-compose down
cd $rootdir/management && docker-compose down
cd $rootdir/networking && docker-compose down
cd $rootdir

