#coding=utf-8
import sys
if sys.version[0]=='3':
    modern=True
elif sys.version[0]=='2':
    modern=False
else:
    raise AssertionError

if modern:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import messagebox
    import threading
else:
    from Tkinter import *
    from ttk import *
    import tkMessageBox as messagebox
    import thread
import os
from time import sleep

proj=''

def log(a,mode=None,enter=True):
    textout.config({'state':'normal'})
    if modern:
        a=str(a)
    else:
        a=unicode(a)
    if mode:
        textout.insert(END,a,mode)
    else:
        textout.insert(END,a)
    if enter:
        textout.insert(END,'\n')
    textout.config({'state':'disabled'})
    textout.see(END)

def cls(*_):
    textout.config({'state':'normal'})
    textout.delete(1.0,END)
    textout.config({'state':'disabled'})

def open_proj():
    def done():
        projtk.title('加载编译器...')
        try:
            global vcc
            import vcc
        except:
            global nobuild
            nobuild=True
        try:
            global winsound
            import winsound
        except:
            global nosnd
            nosnd=True
        projtk.destroy()
    
    def open_now(*_):
        global proj
        proj=openprojname.get()
        if not proj:
            return
        if not os.path.isdir('projects/'+proj) or not os.path.isfile('projects/%s/%s.txt'%(proj,proj)):
            messagebox.showerror('Waver','工程不存在')
            return
        done()

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
        done()
    
    projtk=Tk()
    projtk.title('Waver IDE')
    projtk.resizable(True,False)
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
    if modern:
        openprojc['values']=os.listdir('projects')
    else:
        openprojc['values']=tuple([a.decode('gbk') for a in os.listdir('projects')])
    openprojc.bind('<Return>',open_now)
    openprojc.bind('<<ComboboxSelected>>',open_now)
    openprojc.grid(row=0,column=0,sticky='we',padx=3,pady=2)
    #new
    newproje=Entry(newprojf,textvariable=newprojname)
    newproje.bind('<Return>',new_now)
    newproje.grid(row=0,column=0,sticky='we',padx=3,pady=2)
    #done
    projtk.mainloop()

def refresh():
    try:
        if modern:
            filesli=tuple(filter(
                (lambda x:os.path.splitext(x)[1]=='.txt'),
                os.listdir('projects/'+proj)
                ))
        else:
            filesli=list(filter(
                (lambda x:os.path.splitext(x.decode('gbk')[1]=='.txt')),
                os.listdir('projects/'+proj)
                ))
            for now in range(len(filesli)):
                filesli[now]=filesli[now].decode('gbk')
            filesli=tuple(filesli)
        filesvar.set(filesli)
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While loading file list')

def build(*_):
    #exec
    savefile()
    if nobuild:
        log('Build function disabled','error')
        return
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
            log('While processing: '+(vcc.nowline if vcc.nowline else '(None)'))
        else:
            log('[FINISH]','success')
            playsnd(filenow[:-4])
    if modern:
        threading.Thread(target=execute,args=()).start()
    else:
        thread.start_new_thread(execute,())

def savefile(*_):
    if not filenow:
        return True
    try:
        tex=textin.get(1.0,END)[:-1]
        with open('projects/%s/%s'%(proj,filenow),'w') as f:
            if modern:
                f.write(tex)
            else:
                f.write(tex.encode('utf-8'))
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While saving '+filenow)
        return False
    else:
        log('File saved: '+filenow,'success')
        return True

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
    if not savefile():
        if not messagebox.askyesno('Waver IDE','保存失败,仍要继续吗?\n警告:仍然继续可能会导致内容丢失'):
            return
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
    tk.title('[%s] %s - Waver IDE'%(filenow,proj))

def explorer(*_):
    try:
        os.startfile(os.path.join(os.curdir,'projects/%s'%proj))
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While exploring project folder')

def playsnd(toplay=None):
    if nosnd:
        log('Sound playing function disabled','error')
        return
    if not toplay:
        toplay=os.path.splitext(filenow)[0]
    try:
        winsound.PlaySound('projects/%s/%s.wav'%(proj,toplay),
                           winsound.SND_FILENAME|winsound.SND_NOWAIT|winsound.SND_ASYNC|winsound.SND_PURGE)
    except Exception as e:
        log('[ERROR]','error')
        log(e)
        log('While playing '+toplay)
    else:
        log('Playing '+toplay,'highlight')


def stopsnd(quiting=False):
    if nosnd:
        return
    try:
        winsound.PlaySound(None,winsound.SND_MEMORY|winsound.SND_PURGE)
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

def notebook(*_):
    def notewin():
        def split(*_):
            t.insert(INSERT,'\n')
            t.insert(INSERT,'-----\n','spliter')
        def clear(*_):
            t.delete(1.0,END)
        
        notek=Tk()
        notek.geometry("200x350")
        notek.title('VDE Notebook')
        notek.wm_attributes('-topmost',1)
        f=Frame(notek)
        f.pack(side=TOP)
        Button(f,text='清空',command=clear).pack(side=RIGHT)
        Button(f,text='分隔',command=split).pack(side=LEFT)
        t=Text(notek,background='gray',font='Consolas')
        t.bind('<Control-Return>',split)
        t.bind('<Escape>',clear)
        t.tag_config('spliter',background='yellow')
        t.pack(side=TOP,expand=True,fill='both')
        notek.focus_force()
        notek.mainloop()
    
    tk.newWindow=notewin()

nobuild=False
nosnd=False
open_proj()
if not proj:
    sys.exit(-2048)

tk=Tk()
tk.title('%s - Waver IDE'%proj)
tk.geometry("850x500")
filein=StringVar()
filesvar=StringVar()
filein.set(proj+'.txt')
filenow=''
musictall=0.0
tk.rowconfigure(0,weight=1)
#bind
tk.bind('<Control-s>',savefile)
tk.bind('<Control-S>',savefile)
tk.bind('<Control-b>',explorer)
tk.bind('<Control-B>',explorer)
tk.bind('<Control-n>',notebook)
tk.bind('<Control-N>',notebook)
tk.bind('<F5>',build)
tk.bind('<Escape>',lambda *_:stopsnd())
tk.bind('<Shift-Escape>',cls)
#sidebar
frame=Frame(tk)
frame.grid(row=0,column=0,sticky='ns')
#sidebar-box
filebox=Entry(frame,textvariable=filein)
filebox.bind('<Return>',lambda *_:changefile(fromli=False))
filebox.grid(row=0,column=0,columnspan=2,pady=5,padx=5,sticky='we')
#sidebar-li
fileli=Listbox(frame,listvariable=filesvar)
fileli.bind('<<ListboxSelect>>',lambda *_:changefile(fromli=True))
fileli.grid(row=1,column=0,columnspan=2,pady=5,padx=5,sticky='wens')
frame.rowconfigure(1,weight=1,minsize=5)
#sidebar-btn
Button(frame,text='浏览',command=explorer).grid(row=2,column=0,pady=2)
Button(frame,text='刷新',command=refresh).grid(row=2,column=1,pady=2)
Button(frame,text='播放',command=lambda *_:playsnd()).grid(row=3,column=0,pady=2)
Button(frame,text='停止',command=stopsnd).grid(row=3,column=1,pady=2)
Button(frame,text='生成',command=build).grid(row=4,column=0,pady=2)
Button(frame,text='随记',command=notebook).grid(row=4,column=1,pady=2)
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
white='#FFFFFF'
blue='#0000FF'
black='#000000'
gray='#BEBEBE'
red='#FF0000'
yellow='#FFFF00'
green='#00FF00'
textout=Text(upframe,state='disabled',font='Consolas')
textout.tag_config('comment',foreground=blue,background=white)
textout.tag_config('info',foreground=black,background=gray)
textout.tag_config('goto',foreground=white,background=blue)
textout.tag_config('error',foreground=white,background=red)
textout.tag_config('success',foreground=black,background=green)
textout.tag_config('indent',foreground=blue,background=white)
textout.tag_config('highlight',foreground=black,background=yellow)
textout.grid(row=0,column=2,sticky='nsew')
upframe.columnconfigure(2,weight=2,minsize=400)
#done
log('Waver IDE by xmcp','info')
if nobuild:
    log('Cannot load VCC','error')
    log('Build function will be disabled.','highlight')
if nosnd:
    log('Cannot load winsound','error')
    log('Sound playing function will be disabled','highlight')
refresh()
changefile(fromli=False)
tk.focus_force()
tk.mainloop()
stopsnd(quiting=True)
