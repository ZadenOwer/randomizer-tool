#!/bin/bash
if [ -z "$1" ]
then
   echo "Provide a version number"
   exit 1
fi

echo "Creating executable on: $PWD/dist"

echo "Version $1"

rm -r "$PWD\dist"

python -m PyInstaller \
--onefile \
--clean \
-n randomizer$1 \
index.py

mkdir 'dist'
mkdir 'dist/src'
mkdir 'dist/logs'
mkdir 'dist/src/jsons'
mkdir 'dist/src/statics'
# mkdir 'dist/src/dlls'


cp -R minified/jsons dist/src/
cp -R src/statics dist/src/

# for f in src/dlls/*.dll
# do 
#    cp -v "$f" dist/"${f%.dll}".dll
# done

# for f in src/*.bfbs
# do 
#    cp -v "$f" dist/"${f%.bfbs}".bfbs
# done

cp -v "$PWD\src\static\flatc.exe" "$PWD\dist\src\static\flatc.exe"

rm -r "$PWD\randomizer$1.spec"
rm -r "$PWD\build"

exit 0