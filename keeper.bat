@echo off
title Keeper
color 0f
mode con cols=45 lines=10
set /p proj=Project:
:q
cls
echo Keeping %proj%
waver.py %proj%
pause
goto q