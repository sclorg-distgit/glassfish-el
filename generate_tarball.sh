#!/bin/bash

aid="javax.el"
version=`grep Version: *spec | sed -e 's/Version:\s*\(.*\)/\1/'`
filename="${aid}-${version}-sources.jar"
tempdir="glassfish-el-${version}"
url="http://central.maven.org/maven2/org/glassfish/${aid}/${version}/${aid}-${version}-sources.jar"

echo $version

rm -Rf ${tempdir}
mkdir ${tempdir}

pushd ${tempdir}
  wget ${url}
  unzip ${filename}
  mv META-INF/LICENSE.txt .
  rm -Rf ${filename} META-INF/
  mkdir -p src/main/java
  # upstream bundles el-api in javax/ dir, exclude it
  mv com/ src/main/java
popd

tar czvf glassfish-el-${version}.tar.gz ${tempdir}

rm -Rf ${tempdir}

