#!/bin/bash

echo -e '\nBuilding Application...'

PYTHON_APP=`ls | grep .py$`
APP_ICON=`find . -name '*.ico'`

if [ -d ./build ]; then
	rm -rf ./build
fi

if [ -d ./dist ]; then
	rm -rf ./dist
fi

if [ -f *.spec ]; then
	rm -rf *.spec
fi

pyinstaller --onedir --windowed --icon=${APP_ICON} ${PYTHON_APP}

echo -e '\nDONE!'
