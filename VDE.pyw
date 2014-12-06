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
    openprojf.pack(side=TOP,expand=True)
    newprojf.pack(side=TOP,expand=True)
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
    filebox['values']=filter((lambda x:os.path.splitext(x)[1]=='.txt'),os.listdir('projects/'+proj))

def build():
    #exec
    savefile()
    def execute():
        def loger(a,origin=''):
            if origin.startswith('##'):
                textout.insert(END,str(a)+'\n','comment')
            elif origin.startswith('Buil'):
                textout.insert(END,str(a)+'\n','cmd')
            elif origin.startswith('=> '):
                textout.insert(END,str(a)+'\n','goto')
            elif origin=='[ERROR]' or a=='[ERROR]':
                textout.insert(END,str(a)+'\n','error')
            else:
                textout.insert(END,str(a)+'\n')
            textout.see(END)
        textout.config({'state':'normal'})
        textout.delete(1.0,END)
        loger('Loading Waver Compiler...')
        try:
            vcc.process(proj,proj,logcallback=loger)
        except AssertionError:
            pass
        except Exception as e:
            loger('[ERROR]')
            loger(e)
            loger('While processing: '+vcc.nowline)
        else:
            loger('[FINISH]')
            sleep(0.25)
            os.startfile(os.path.join(os.curdir,'projects/%s/%s.wav'%(proj,proj)))
        finally:
            textout.config({'state':'disabled'})
    try:
        import threading
        threading.Thread(target=execute,args=()).start()
    except ImportError:
        import thread
        thread.start_new_thread(execute,())

def savefile():
    if not filenow:
        return
    with open('projects/%s/%s'%(proj,filenow),'w') as f:
        f.write(textin.get(1.0,END)[:-1])

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
        with open(filen,'r') as f:
            textin.delete(1.0,END)
            textin.insert(1.0,f.read())
    else:
        if messagebox.askyesno('Waver','文件不存在,是否创建?'):
            with open(filen,'w') as f:
                f.write('# Write here.\n')
            with open(filen,'r') as f:
                textin.delete(1.0,END)
                textin.insert(1.0,f.read())
            refresh()
    filenow=filein.get()

open_proj()
if not proj:
    sys.exit(-2048)

tk=Tk()
tk.title('%s - Waver IDE'%proj)
filein=StringVar()
filenow=''
#frame
upframe=Frame(tk)
upframe.pack(side=TOP)
textin=Text(upframe)
textin.pack(side=LEFT)
sbar=Scrollbar(upframe,orient=VERTICAL,command=textin.yview)
sbar.pack(side=RIGHT,fill='both')
textin['yscrollcommand']=sbar.set
frame=Frame(tk)
frame.pack(side=TOP,fill='both')
#objs
Button(frame,text='生成',command=build).pack(side=RIGHT,pady=5)
filebox=Combobox(frame,textvariable=filein)
refresh()
filebox.bind('<<ComboboxSelected>>',changefile)
filebox.pack(side=LEFT)
Button(frame,text='打开',command=changefile).pack(side=LEFT)
#status
downframe=Frame(tk)
downframe.pack(side=TOP)
textout=Text(downframe,height=10,state='disabled')
textout.tag_config('comment',foreground='blue')
textout.tag_config('cmd',foreground='red')
textout.tag_config('goto',background='green')
textout.tag_config('error',foreground='white',background='black')
textout.pack(side=LEFT)
outsbar=Scrollbar(downframe,orient=VERTICAL,command=textout.yview)
outsbar.pack(side=RIGHT,fill='both')
textout['yscrollcommand']=outsbar.set
import vcc
tk.mainloop()
