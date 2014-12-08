#coding=utf-8
try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkMessageBox as messagebox

import os
import sys
from time import sleep
proj=''

def log(a,mode=None):
    textout.config({'state':'normal'})
    if mode:
        textout.insert(END,str(a)+'\n',mode)
    else:
        textout.insert(END,str(a)+'\n')
    textout.config({'state':'disabled'})
    textout.see(END)

def open_proj():
    def open_now():
        global proj
        proj=openprojname.get()
        if not proj:
            return
        if not os.path.isdir('projects/'+proj) or not os.path.isfile('projects/%s/%s.txt'%(proj,proj)):
            messagebox.showerror('Waver','工程不存在')
            return
        projtk.destroy()

    def new_now():
        global proj
        proj=newprojname.get()
        if not proj:
            return
        if os.path.isdir('projects/'+proj):
            messagebox.showerror('Waver','工程已经存在')
            return
        os.makedirs('projects/'+proj)
        with open('projects/%s/%s.txt'%(proj,proj),'w') as f:
            f.write('# Write here.\n')
        projtk.destroy()
    
    projtk=Tk()
    projtk.title('Waver IDE')
    projtk.resizable(False,False)
    newprojname=StringVar()
    openprojname=StringVar()
    #frame
    openprojf=Labelframe(projtk,text='打开')
    newprojf=Labelframe(projtk,text='新建')
    openprojf.pack(side=TOP,expand=True,padx=5,pady=5)
    newprojf.pack(side=TOP,expand=True,padx=5,pady=5)
    #open
    openprojc=Combobox(openprojf,textvariable=openprojname)
    openprojc['values']=os.listdir('projects')
    openprojc.pack(side=LEFT)
    Button(openprojf,text='打开',command=open_now).pack(side=RIGHT)
    #new
    Entry(newprojf,textvariable=newprojname).pack(side=LEFT,padx=9)
    Button(newprojf,text='新建',command=new_now).pack(side=RIGHT)
    #loop
    projtk.mainloop()

def refresh():
    try:
        filebox['values']=filter((lambda x:os.path.splitext(x)[1]=='.txt'),os.listdir('projects/'+proj))
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While loading file list')

def build(*_):
    #exec
    savefile()
    def execute():
        def loger(a,origin=''):
            if origin.startswith('##'):
                log(a,'comment')
            elif origin.startswith('Buil'):
                log(a,'info')
            elif origin.startswith('=> '):
                log(a,'goto')
            elif origin=='[ERROR]' or a=='[ERROR]':
                log(a,'error')
            else:
                log(a)
        textout.config({'state':'normal'})
        textout.delete(1.0,END)
        log('Loading Waver Central Compiler (VCC)','info')
        try:
            vcc.process(proj,proj,logcallback=loger)
        except AssertionError:
            pass
        except Exception as e:
            log('[ERROR]','error')
            log(e)
            log('While processing: '+vcc.nowline)
        else:
            log('[FINISH]','success')
            sleep(0.25)
            os.startfile(os.path.join(os.curdir,'projects/%s/%s.wav'%(proj,proj)))
    try:
        import threading
        threading.Thread(target=execute,args=()).start()
    except ImportError:
        import thread
        thread.start_new_thread(execute,())

def savefile(*_):
    if not filenow:
        return
    try:
        with open('projects/%s/%s'%(proj,filenow),'w') as f:
            f.write(textin.get(1.0,END)[:-1])
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While saving '+filenow)
    else:
        log('File saved: '+filenow,'success')

def changefile(*_):
    if not filein.get():
        return
    if os.path.splitext(filein.get())[1]!='.txt':
        messagebox.showerror('Waver','扩展名必须为.txt')
        return
    savefile()
    global filenow
    filen='projects/%s/%s'%(proj,filein.get())
    if os.path.isfile(filen):
        try:
            with open(filen,'r') as f:
                textin.delete(1.0,END)
                textin.insert(1.0,f.read())
        except Exception as e:
            log('[ERROR]','error')
            log(e)
            log('While opening '+filen)
    else:
        if messagebox.askyesno('Waver','文件不存在,是否创建?'):
            try:
                with open(filen,'w') as f:
                    f.write('# Write here.\n')
                with open(filen,'r') as f:
                    textin.delete(1.0,END)
                    textin.insert(1.0,f.read())
            except Exception as e:
                log('[ERROR]','error')
                log(e)
                log('While creating '+filen)
            refresh()
    filenow=filein.get()

open_proj()
if not proj:
    sys.exit(-2048)

tk=Tk()
tk.title('%s - Waver IDE'%proj)
tk.resizable(False,False)
filein=StringVar()
filenow=''
tk.bind('<Control-s>',savefile)
tk.bind('<F5>',build)
#left
upframe=Frame(tk)
upframe.pack(side=TOP)
textin=Text(upframe,width=50,height=30)
textin.pack(side=LEFT)
sbar=Scrollbar(upframe,orient=VERTICAL,command=textin.yview)
sbar.pack(side=LEFT,fill='both')
textin['yscrollcommand']=sbar.set
frame=Frame(tk)
frame.pack(side=TOP,fill='both')
#right
textout=Text(upframe,state='disabled',width=50,height=30)
textout.tag_config('comment',foreground='green')
textout.tag_config('info',background='gray')
textout.tag_config('goto',background='green')
textout.tag_config('error',foreground='white',background='red')
textout.tag_config('success',foreground='black',background='green')
textout.pack(side=LEFT)
#objs
Button(frame,text='生成',command=build).pack(side=RIGHT,pady=5,padx=5)
filebox=Combobox(frame,textvariable=filein)
refresh()
filebox.bind('<<ComboboxSelected>>',changefile)
filebox.bind('<Return>',changefile)
filebox.pack(side=LEFT,padx=5)
Button(frame,text='打开',command=changefile).pack(side=LEFT)
import vcc
log('Waver IDE by xmcp','info')
tk.mainloop()
