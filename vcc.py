#coding=utf-8
if __name__=='__main__':
    print('Loading Waver Compiler by xmcp...')

import sys
if sys.version[0]=='2':
    range=xrange
    input=raw_input

import libwaver as waver
import os
from time import sleep

nowline='(None)'
def process(proj,workdir,f=None,parent='ROOT',parentlevel=0,logcallback=None):
    def log(stuff,istop=False):
        if istop:
            outstr=stuff
        else:
            outstr='.'*(parentlevel*2)+stuff
        if logcallback==None:
            print(outstr)
        else:
            logcallback(outstr,stuff)
    
    global nowline
    log('Building %s->%s'%(parent,proj))
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
            process(line[3:],workdir,f,'%s->%s'%(parent,proj),parentlevel+1,logcallback)
            continue
        rate=line.split('\t')[0]
        time=float(line.split('\t')[1])/4
        f.write(waver.ratable[rate],time)
    log('Built %s->%s'%(parent,proj))
    f.close()

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
        sleep(0.25)
        os.startfile(os.path.join(os.curdir,'projects/%s/%s.wav'%(proj,proj)))

