@echo off
title Keeper
color 0f
mode con cols=50 lines=25
:init
cls
set /p proj=Project:
title %proj% - Keeper
:q
cls
vcc.py "%proj%"
start "" "projects/%proj%/%proj%.wav"
pause
goto q