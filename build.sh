#!/usr/bin/env bash
REPO='my/myhoney/'
clear
cd $HOME/$REPO
echo "================================= CLEAR START ==============================="
rm -rf build
rm -rf dist
echo "OK"
echo "========================== Building from .spec START ========================"
$HOME/.wine/drive_c/Python27/python.exe -m PyInstaller -y --clean --onefile --noconsole --nowindowed --name Honey --icon images/system/favicon.ico Main.spec
echo "============================= LAUNCHING EXE START ==========================="
cd dist
wine Honey.exe