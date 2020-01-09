#!/bin/bash 

VERSION=2019-09-05_20-10
curl -L -O -s https://github.com/The-OpenROAD-Project/alpha-release/releases/download/v${VERSION}/OpenROAD-${VERSION}.tar.gz
tar xfz OpenROAD-${VERSION}.tar.gz
ln -s openroad/OpenROAD-2019-09-05_20-10/bin latest
