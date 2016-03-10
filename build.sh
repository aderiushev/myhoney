#!/usr/bin/env bash
clear
cd /home/aleksei/my/myhoney/
echo "================================= CLEAR START ==============================="
rm -rf build
rm -rf dist
echo "OK"
echo "========================== Building from .spec START ========================"
/home/aleksei/.wine/drive_c/Python27/python.exe -m PyInstaller -y --clean --onefile --noconsole --nowindowed --name Honey --icon favicon.ico Main.spec
echo "============================= LAUNCHING EXE START ==========================="
cd dist
wine Honey.exe