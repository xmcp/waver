#coding=utf-8
try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import messagebox
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkMessageBox as messagebox
try:
    from winsound import *
except:
    pass
import os
import sys
from time import sleep
proj=''

def log(a,mode=None,enter=True):
    textout.config({'state':'normal'})
    if mode:
        textout.insert(END,str(a),mode)
    else:
        textout.insert(END,str(a))
    if enter:
        textout.insert(END,'\n')
    textout.config({'state':'disabled'})
    textout.see(END)

def cls(*_):
    textout.config({'state':'normal'})
    textout.delete(1.0,END)
    textout.config({'state':'disabled'})

def open_proj():
    def open_now(*_):
        global proj
        proj=openprojname.get()
        if not proj:
            return
        if not os.path.isdir('projects/'+proj) or not os.path.isfile('projects/%s/%s.txt'%(proj,proj)):
            messagebox.showerror('Waver','工程不存在')
            return
        projtk.destroy()

    def new_now(*_):
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
    openprojname.set('选择工程……')
    #frame
    openprojf=Labelframe(projtk,text='打开')
    newprojf=Labelframe(projtk,text='新建')
    openprojf.grid(row=0,column=0,sticky='we',padx=5,pady=5)
    newprojf.grid(row=1,column=0,sticky='we',padx=5,pady=5)
    projtk.columnconfigure(0,weight=1)
    openprojf.columnconfigure(0,weight=1)
    newprojf.columnconfigure(0,weight=1)
    #open
    openprojc=Combobox(openprojf,textvariable=openprojname)
    openprojc['values']=os.listdir('projects')
    openprojc.bind('<Return>',open_now)
    openprojc.bind('<<ComboboxSelected>>',open_now)
    openprojc.grid(row=0,column=0,sticky='we',padx=3,pady=2)
    #new
    newproje=Entry(newprojf,textvariable=newprojname)
    newproje.bind('<Return>',new_now)
    newproje.grid(row=0,column=0,sticky='we',padx=3,pady=2)
    #loop
    projtk.mainloop()

def refresh():
    try:
        filesli=tuple(filter(
            (lambda x:os.path.splitext(x)[1]=='.txt'),os.listdir('projects/'+proj)
            ))
        filesvar.set(filesli)
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While loading file list')

def build(*_):
    #exec
    savefile()
    def execute():
        global musictall
        def loger(a,origin=None,indent=0):
            a=str(a)
            if not origin:
                origin=a
            origin=str(origin)
            if indent:
                log('.'*(2*indent),'indent',enter=False)
            if origin.startswith('##'):
                log(origin,'comment')
            elif origin.startswith('Built'):
                log(origin,'info')
            elif origin.startswith('=> '):
                log(origin,'goto')
            elif origin=='[ERROR]' or a=='[ERROR]':
                log(origin,'error')
            else:
                log(a)
        cls()
        log('Loading Waver Central Compiler (VCC)')
        try:
            musictall=vcc.process(filenow[:-4],proj,logcallback=loger)
        except AssertionError:
            pass
        except Exception as e:
            log('[ERROR]','error')
            log(e)
            log('While processing: '+vcc.nowline)
        else:
            log('[FINISH]','success')
            playsnd(filenow[:-4])
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

def changefile(fromli):
    if fromli:
        try:
            fileno=fileli.selection_get()
            filen='projects/%s/%s'%(proj,fileno)
        except Exception as e:
            log('[ERROR]','error')
            log(e)
            log('While opening '+filen)
    else: #from text
        fileno=filein.get()
        if not fileno:
            return
        if os.path.splitext(fileno)[1]!='.txt':
            messagebox.showerror('Waver','扩展名必须为.txt')
            return
        filen='projects/%s/%s'%(proj,fileno)
    savefile()
    global filenow
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
    filenow=fileno
    tk.title('[%s] %s - Wave IDE'%(filenow,proj))

def playsnd(toplay=None):
    if not toplay:
        toplay=os.path.splitext(filenow)[0]
    try:
        PlaySound('projects/%s/%s.wav'%(proj,toplay),SND_FILENAME|SND_NOWAIT|SND_ASYNC|SND_PURGE)
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While playing '+toplay)
    else:
        log('Playing '+toplay,'highlight')


def stopsnd(quiting=False):
    try:
        PlaySound(None,SND_MEMORY|SND_PURGE)
    except Exception as e:
        if quiting:
            raise
        else:
            log('[ERROR]','error')
            log(e)
            log('While trying to stop sound')
    else:
        if not quiting:
            log('Music killed','info')

open_proj()
if not proj:
    sys.exit(-2048)

tk=Tk()
tk.title('%s - Waver IDE'%proj)
filein=StringVar()
filesvar=StringVar()
filein.set(proj+'.txt')
filenow=''
musictall=0.0
tk.rowconfigure(0,weight=1)
#bind
tk.bind('<Control-s>',savefile)
tk.bind('<Control-S>',savefile)
tk.bind('<F5>',build)
tk.bind('<Escape>',lambda *_:stopsnd())
tk.bind('<Shift-Escape>',cls)
#sidebar
frame=Frame(tk)
frame.grid(row=0,column=0,sticky='ns')
#sidebar-box
filebox=Entry(frame,textvariable=filein)
filebox.bind('<Return>',lambda *_:changefile(fromli=False))
filebox.grid(row=0,column=0,pady=5,padx=5)
#sidebar-li
fileli=Listbox(frame,listvariable=filesvar)
fileli.bind('<<ListboxSelect>>',lambda *_:changefile(fromli=True))
fileli.grid(row=1,column=0,pady=5,padx=5,sticky='ns')
frame.rowconfigure(1,weight=1,minsize=5)
#sidebar-btn
Button(frame,text='生成',command=build).grid(row=2,column=0,pady=5,padx=5)
Button(frame,text='停止',command=stopsnd).grid(row=3,column=0,pady=5,padx=5)
Button(frame,text='播放',command=lambda *_:playsnd()).grid(row=4,column=0,pady=5,padx=5)
#mainpart
upframe=Frame(tk)
upframe.grid(row=0,column=1,sticky='nsew')
tk.columnconfigure(1,weight=1)
upframe.rowconfigure(0,weight=1)
#mainpart-textin
textin=Text(upframe,font='Consolas')
textin.grid(row=0,column=0,sticky='nsew')
upframe.columnconfigure(0,weight=1,minsize=200)
sbar=Scrollbar(upframe,orient=VERTICAL,command=textin.yview)
sbar.grid(row=0,column=1,sticky='ns')
textin['yscrollcommand']=sbar.set
#mainpart-textout
textout=Text(upframe,state='disabled',font='Consolas')
textout.tag_config('comment',foreground='blue',background='white')
textout.tag_config('info',foreground='black',background='gray')
textout.tag_config('goto',foreground='white',background='blue')
textout.tag_config('error',foreground='white',background='red')
textout.tag_config('success',foreground='black',background='green')
textout.tag_config('indent',foreground='blue',background='white')
textout.tag_config('highlight',foreground='black',background='yellow')
textout.grid(row=0,column=2,sticky='nsew')
upframe.columnconfigure(2,weight=2,minsize=400)
#done
import vcc
log('Waver IDE by xmcp','info')
refresh()
changefile(fromli=False)
tk.mainloop()
stopsnd(quiting=True)
