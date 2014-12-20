#coding=utf-8
import sys
if sys.version[0]=='2':
    input=raw_input

import os
import msvcrt

os.system('title Keeper')
print('Loading vcc...')
import vcc

proj=input('Project name:')
os.system('title %s - Keeper'%proj)
while True:
    os.system('cls')
    print('[ Keeping %s ]'%proj)
    vcc.process(proj,proj)
    os.startfile(os.path.join(os.curdir,'projects/%s/%s.wav'%(proj,proj)))
    print('[ Finished ]')
    msvcrt.getch()
