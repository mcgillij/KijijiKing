#!/bin/bash
#pyrcc4.exe feedpy_rc.qrc > feedpy_rc.py
pyuic4.sh main_window.ui -o main_window.py
pyuic4.sh settings_diag.ui -o settings_diag.py

