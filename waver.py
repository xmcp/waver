#coding=utf-8

import sys
if sys.version[0]=='2':
    range=xrange
    input=raw_input

import libwaver as waver

proj=input('Project Name:')
with open('projects/%s.txt'%proj,'r') as f:
    lines=f.read().split('\n')

try:
    lines=lines[lines.index('[START]')+1:]
except (ValueError,IndexError):
    pass
else:
    print('[START] Trigger Found.')

f=waver.wavefile('projects/%s.wav'%proj)
for line in lines:
    if not line or line[0]=='#':
        continue
    if line=='[STOP]':
        break
    rate=line.split('\t')[0]
    time=float(line.split('\t')[1])/4
    f.write(waver.ratable[rate],time)
f.close()
print('done')
