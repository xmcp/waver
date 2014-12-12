#coding=utf-8
from __future__ import division

if __name__=='__main__':
    print('Waver Central Compiler (VCC) by xmcp')

import sys
if sys.version[0]=='2':
    range=xrange
    input=raw_input

import libwaver as waver
import os
from time import sleep

ratable={
    '0':0,
    '-1':262,'-2':294,'-3':330,'-4':349,'-5':392,'-6':440,'-7':494,
    'L1':262,'L2':294,'L3':330,'L4':349,'L5':392,'L6':440,'L7':494,
    '1':523,'2':587,'3':659,'4':699,'5':784,'6':880,'7':988,
    '+1':1047,'+2':1175,'+3':1319,'+4':1397,'+5':1568,'+6':1760,'+7':1976,
    'H1':1047,'H2':1175,'H3':1319,'H4':1397,'H5':1568,'H6':1760,'H7':1976,
    '-2b':277,'-3b':311,'-5b':370,'-6b':415,'-7b':466,
    'L2b':277,'L3b':311,'L5b':370,'L6b':415,'L7b':466,
    '2b':554,'3b':622,'5b':740,'6b':830,'7b':932,
    '+2b':1108,'+3b':1244,'+5b':1479,'+6b':1661,'+7b':1864,
    'H2b':1108,'H3b':1244,'H5b':1479,'H6b':1661,'H7b':1864,
}

nowline='(None)'
def process(proj,workdir,f=None,parentlevel=0,logcallback=None):
    def log(stuff,istop=False):
        if istop:
            outstr=stuff
        else:
            outstr='.'*(parentlevel*2)+stuff
        if logcallback==None:
            print(outstr)
        else:
            logcallback(outstr,stuff,parentlevel)
    
    global nowline
    if parentlevel>10:
        log('[ERROR]',True)
        log('Call stack upper limit exceeded.',True)
        raise AssertionError
    
    if not f:
        f=waver.wavefile('projects/%s/%s.wav'%(workdir,proj))
    #load file
    try:
        with open('projects/%s/%s.txt'%(workdir,proj),'r') as fi:
            lines=fi.read().split('\n')
    except Exception as e:
        log('[ERROR]',True)
        log(e,True)
        log('While reading project.',True)
        raise AssertionError
    #find start
    try:
        lines=lines[lines.index('[START]')+1:]
    except (ValueError,IndexError):
        pass
    else:
        log('[START] Trigger Found.')
    #process!
    for line in lines:
        nowline=line
        if not line:
            continue
        if line[0]=='#':
            if line[1]=='#':
                log(line)
            continue
        if line=='[STOP]':
            log('[STOP] Trigger Found.')
            break
        if line.startswith('=> '):
            log(line)
            process(line[3:],workdir,f,parentlevel+1,logcallback)
            continue
        splited=line.split('\t')
        if len(splited)==1:
            rate=splited[0]
            time=1/4
        elif len(splited)==2:
            rate=splited[0]
            time=float(splited[1])/4
        else:
            log('[ERROR]')
            log('Invalid syntax.')
            log('While processing: '+line)
            raise AssertionError
        f.write(ratable[rate],time)
    log('Built %s'%proj)
    f.close()
    return f.gettotaltime()

if __name__=='__main__':
    #open file
    if len(sys.argv)==2:
        proj=sys.argv[1]
    else:
        proj=input('Project Name: ')
    
    try:
        process(proj,proj)
    except AssertionError:
        pass
    except Exception as e:
        print('[ERROR]')
        print(e)
        print('While processing: '+nowline)
    else: #done
        print('[FINISH]')

