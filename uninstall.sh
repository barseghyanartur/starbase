pip uninstall starbase -y
rm build -rf
rm dist -rf
find . -name '*.pyc' -delete
find . -name '__pycache__' -delete
rm src/starbase.egg-info -rf
rm builddocs.zip