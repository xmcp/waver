#coding=utf-8
from __future__ import division
import wave
import numpy as np

class wavefile(object):
    _framerate=16384
    _volumn=15000
    _tall=0
    
    f=None
    data=''
    
    def __init__(self,fname):
        if fname:
            self.f=wave.open(fname,'wb')
            self.f.setnchannels(1)
            self.f.setsampwidth(2)
            self.f.setframerate(self._framerate)
        else:
            self.data=''
        self._tall=0
        
    def write_bin(self,rate,time):
        dt=1./self._framerate
        #print(rate,time)
        if rate>1e-5:
            w=np.arange(0,time*2*np.pi*rate,dt*2*np.pi*rate)
            wave_data=(self._volumn*np.sin(w)).astype(np.short)
        else:
            wave_data=np.zeros((round(time/dt),),dtype=np.short)
        if self.f:
            self.f.writeframes(wave_data.tostring())
        else:
            self.data+=wave_data.tostring()
        self._tall+=time

    def write(self,rate,time):
        if rate!=0:
            ratet=1/rate
            t1=ratet-self._tall%ratet
            self.write_bin(0,t1) #prefix
            time-=t1
            t1=time*7/8+ratet-(time*7/8)%ratet
            self.write_bin(rate,t1) #main
            if time-t1>0:
                self.write_bin(0,time-t1) #suffix
        else:
            self.write_bin(0,time)

    def gettotaltime(self):
        return self._tall

    def close(self):
        if self.f==None:
            return False
        else:
            try:
                self.f.flush()
                self.f.close()
            except:
                pass
            return True
