@echo off
title Keeper
color 0f
mode con cols=45 lines=10
:init
cls
set /p proj=Project:
title %proj% - Keeper
:q
cls
waver.py "%proj%"
pause
goto q