#!/bin/bash
if [ -z "$1" ]
then
   echo "Provide a version number"
   exit 1
fi

echo "Creating executable on: $PWD/dist"

echo "Version $1"

rm -r "$PWD\build"
rm -r "$PWD\dist"

pyinstaller \
--onefile \
--clean \
-n randomizer$1 \
index.py

mkdir 'dist'
mkdir 'dist/src'
mkdir 'dist/src/jsons'

for f in src/jsons/*.json
do 
   cp -v "$f" dist/"${f%.json}".json
done

cp -v "$PWD\src\flatc.exe" "$PWD\dist\src\flatc.exe"
cp -v "$PWD\src\pokedata_array.bfbs" "$PWD\dist\src\pokedata_array.bfbs"

rm -r "$PWD\randomizer$1.spec"
rm -r "$PWD\build"

exit 0