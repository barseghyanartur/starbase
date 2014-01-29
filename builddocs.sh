./uninstall.sh
reset
./install.sh
reset
cat README.rst docs/documentation.rst.distrib > docs/index.rst
sphinx-build -n -a -b html docs builddocs
cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..