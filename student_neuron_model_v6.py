
#you might need to set the path with export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python/site-packages first
#good tutorial for using neuron with python here: https://romaincaze.files.wordpress.com/2015/06/neuron_tuto.pdf
import neuron 
import matplotlib
import subprocess
from neuron import load_mechanisms
import Tkinter as tk
#from Tkinter import ttk #makes nicer looking stuff
matplotlib.use("TkAgg") #matplot lib backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
LARGE_FONT=("Arial",12)
maxNa=.12
maxK=.036
maxLeak=.0003
injcurrent1=.1
injcurrent2=0
delay1=100
delay2=200
dur1=100
dur2=100
NaRev=50
KRev=-77
LeakRev=-54.3
time=np.zeros(12002)
voltage=np.zeros(12002)
cellnum=0
colors=['b','r','g','k','m']
legendlist=list()
class cell(object):
	def __init__(self,Na,K,Leak,NaV,KV,LV):
		self.Na=Na
		self.K=K
		self.Leak=Leak
		self.NaV=NaV
		self.KV=KV
		self.LV=LV
		print "Na:"+str(type(self.Na))
		print "K:"+str(type(self.K))
		print "Leak:"+str(type(self.Leak))
		self.make_sections()
		self.connsect()
		self.biophys()
		

	def make_sections(self):
		self.soma=neuron.h.Section(name='soma',cell=self)
		self.dend=neuron.h.Section(name='dend',cell=self)
	def connsect(self):
		self.dend.connect(self.soma(0.5))
		
	def biophys(self):
		
		self.soma.nseg=1
		self.soma.diam=10
		self.soma.L=10
		self.soma.Ra=125
		self.soma.insert("hh")
		#self.soma.insert("ca_ion")
      		#self.soma.cascale_aabBK = .01
		
		#self.soma.ca_i_Ca=.1
		self.dend.nseg=5
		self.dend.L=300
		self.dend.diam=0.5
		self.dend.Ra=125
		self.dend.insert("pas")
		self.soma.gkbar_hh=self.K
		self.soma.gnabar_hh=self.Na
		self.soma.gl_hh=self.Leak
		self.soma.ena=self.NaV
		self.soma.ek=self.KV
		self.soma.el_hh=self.LV
"""
		self.soma.gakbar_aabBK = self.alphacond #original .05
		self.soma.gabkbar_aabBK = self.alphabetacond
"""

"""
		if self.calcium:
			self.soma.glcabar_Ca=0.0018#original .0018
			self.soma.gtcabar_Ca=0
			self.soma.gncabar_Ca=0
			print "entered calium if"
			#neuron.h.ion_style(self.soma.ca_ion,3,0,0,0,1)
			#self.soma.ca_i_Ca=10000
		else:
			self.soma.glcabar_Ca=0#original .0018
			self.soma.gtcabar_Ca=0
			self.soma.gncabar_Ca=0
			#self.soma.ca_i_Ca=0

			print "entered no calcium if"
"""

		
def runsimulation(legtext,amp1,amp2,dur1,dur2,start1,start2):
	def recvolt(seg):
		rec_v=neuron.h.Vector()
		rec_v.record(seg._ref_v)
		return rec_v

	def rectime(seg):
		rec_t=neuron.h.Vector()
		rec_t.record(seg._ref_t)
		return rec_t


	def setstim(seg,amp,duration,start):
		stim=neuron.h.IClamp(seg(0.5))
		stim.delay=start
		stim.dur=duration
		stim.amp=amp
		return stim

	load_mechanisms("/home/ben/boxing_bk/neuron_model/downloaded_models/Figure5/")


		
	#neuron.h.create soma
	cell1=cell(maxNa,maxK,maxLeak,NaRev,KRev,LeakRev)

	rec_v_cell1=recvolt(cell1.soma(0.5))





	###SPECIFY THE VALUES OF THE SECTION TO BE RECORDED##
	#record time from NEURON (neuron.h._ref_t)
	rec_t=neuron.h.Vector()
	rec_t.record(neuron.h._ref_t)
	#record voltage from center of the soma

	#for i in dends:



	cell1_stim=setstim(cell1.soma,amp1,dur1,start1)
	cell1_stim2=setstim(cell1.soma,amp2,dur2,start2)


	'''ATTRIBUTES OF ELECTRODE
	amp: Amplitude of the injected current
	delay: Time of activation in ms
	dur: Duration of the stimulation
	'''

	#initialize the value of the voltage
	neuron.h.finitialize(-65)
	#set time of the simulation
	tstop=300

	#create ndendrites
	ndend=1
	dends=range(ndend)



	#Run the simulation
	neuron.run(tstop)



	#PLOT THE RESULT
	time=rec_t.as_numpy()


	cell1_volt=rec_v_cell1.as_numpy()

	
	plt.plot(time,cell1_volt,color=colors[cellnum],linewidth=3.0)
	legendlist.append(legtext)

	plt.legend(legendlist)
	global cellnum
	if cellnum==4:
		cellnum=0
	else:
		cellnum=cellnum+1
		
	#plt.plot(time,cell2_volt,color='k',linewidth=3.0)
	plt.xlabel("Time (ms)")
	plt.ylabel("Voltage (mV)")

	#plt.axis(xmin=210,xmax=216,\
		 #ymin=min(cell1_volt)-5,ymax=max(cell1_volt)+5)

	plt.show()
	print "cell1 calcium:"+str(cell1.calcium)
	print "cell2 calcium:"+str(cell2.calcium)
	print "cell1 ca conductance:"+str(cell1.soma.glcabar_Ca)
	print "cell2 ca conductance:"+str(cell2.soma.glcabar_Ca)
	#print neuron.h.psection(sec=cell1.soma)
	#print neuron.h.psection(sec=cell2.soma)
	#print "ca_ion:"+str(cell1.soma.ca_ion)
	










class ui_window(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		container=tk.Frame(self)
		container.pack(side="top",fill="both",expand=True)
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
		self.frames={}
		#for F in (StartPage):
		frame=StartPage(container,self)
		self.frames[StartPage]=frame
		frame.grid(row=0,column=0,sticky="nsew")
		self.show_frame(StartPage)
	def show_frame(self,cont):
		frame=self.frames[cont]
		frame.tkraise() #raise to front


class StartPage(tk.Frame):
	def __init__(self,parent,controller):
		
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Set Parameters",font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		#button2=tk.Button(self,text="Visit Page 2",command=lambda: controller.show_frame(PageTwo))
		#button2.pack()
		#button3=tk.Button(self,text="Graph Page",command=lambda: controller.show_frame(PageThree))
		#button3.pack()
		labeltextNa=tk.StringVar()
		labeltextNa.set("Max Na conductance (S/cm^2)")
		labeldirNa=tk.Label(self,textvariable=labeltextNa,height=4)
		labeldirNa.pack(side="top")
		self.eNa=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eNa.focus_set()
		self.eNa.pack(side="top")
		self.eNa.insert(0,maxNa)
######################################################################################
		labeltextNaRev=tk.StringVar()
		labeltextNaRev.set("Na Reversal Potential (mV)")
		labeldirNaRev=tk.Label(self,textvariable=labeltextNaRev,height=4)
		labeldirNaRev.pack(side="top")
		self.eNaRev=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eNaRev.focus_set()
		self.eNaRev.pack(side="top")
		self.eNaRev.insert(0,NaRev)
		#self.bNa=tk.Button(self,text="set",command=lambda: self.callback("Na"))
		#self.bNa.pack(side="top")
#########################################################################################
		labeltextK=tk.StringVar()
		labeltextK.set("Max K conductance (S/cm^2)")
		labeldirK=tk.Label(self,textvariable=labeltextK,height=4)
		labeldirK.pack(side="top")
		self.eK=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eK.focus_set()
		self.eK.pack(side="top")
		self.eK.insert(0,maxK)
		#self.bK=tk.Button(self,text="set",command=lambda: self.callback("K"))
		#self.bK.pack(side="top")
#########################################################################################
		labeltextKRev=tk.StringVar()
		labeltextKRev.set("K Reversal Potential (mV)")
		labeldirKRev=tk.Label(self,textvariable=labeltextKRev,height=4)
		labeldirKRev.pack(side="top")
		self.eKRev=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eKRev.focus_set()
		self.eKRev.pack(side="top")
		self.eKRev.insert(0,KRev)
#########################################################################################
		labeltextLeak=tk.StringVar()
		labeltextLeak.set("Max Leak conductance (S/cm^2)")
		labeldirLeak=tk.Label(self,textvariable=labeltextLeak,height=4)
		labeldirLeak.pack(side="top")
		self.eLeak=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eLeak.focus_set()
		self.eLeak.pack(side="top")
		self.eLeak.insert(0,maxLeak)
#########################################################################################
		labeltextLeakRev=tk.StringVar()
		labeltextLeakRev.set("Leak Reversal Potential (mV)")
		labeldirLeakRev=tk.Label(self,textvariable=labeltextLeakRev,height=4)
		labeldirLeakRev.pack(side="top")
		self.eLeakRev=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eLeakRev.focus_set()
		self.eLeakRev.pack(side="top")
		self.eLeakRev.insert(0,LeakRev)
#########################################################################################
		labeltextCurrent=tk.StringVar()
		labeltextCurrent.set("Injected Current (nA)")
		labeldirCurrent=tk.Label(self,textvariable=labeltextCurrent,height=4)
		labeldirCurrent.pack(side="top")
		self.eCurrent=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eCurrent.focus_set()
		self.eCurrent.pack(side="top")
		self.eCurrent.insert(0,injcurrent1)
#########################################################################################
		labeltextdelay1=tk.StringVar()
		labeltextdelay1.set("Stim delay1 (ms)")
		labeldirdelay1=tk.Label(self,textvariable=labeltextdelay1,height=4)
		labeldirdelay1.pack(side="top")
		self.edelay1=tk.Entry(self,textvariable=None,width=10)
		self.edelay1.focus_set()
		self.edelay1.pack(side="top")
		self.edelay1.insert(0,delay1)


#########################################################################################
		labeltextCurrent2=tk.StringVar()
		labeltextCurrent2.set("Injected Current 2 (nA)")
		labeldirCurrent2=tk.Label(self,textvariable=labeltextCurrent2,height=4)
		labeldirCurrent2.pack(side="top")
		self.eCurrent2=tk.Entry(self,textvariable=None,width=10)
		#self.e.insert(0,9000)
		self.eCurrent2.focus_set()
		self.eCurrent2.pack(side="top")
		self.eCurrent2.insert(0,injcurrent2)
#########################################################################################
		labeltextdelay2=tk.StringVar()
		labeltextdelay2.set("Stim delay2 (ms)")
		labeldirdelay2=tk.Label(self,textvariable=labeltextdelay2,height=4)
		labeldirdelay2.pack(side="top")
		self.edelay2=tk.Entry(self,textvariable=None,width=10)
		self.edelay2.focus_set()
		self.edelay2.pack(side="top")
		self.edelay2.insert(0,delay2)

		#self.bLeak=tk.Button(self,text="set",command=lambda: self.callback("Leak"))
		#self.bLeak.pack(side="top")
		self.runbutton=tk.Button(self,text="Run Simulation",command=lambda: self.callback())
		self.runbutton.pack(side="top")
		#button1=tk.Button(self,text="Plot",command=lambda: controller.show_frame(PageOne))
		#button1.pack(side="top")
		self.defaultsbutton=tk.Button(self,text="Reset to Defaults",command=lambda: self.setdefaults())
		self.defaultsbutton.pack(side="top")

		self.closebutton=tk.Button(self,text="Close Window/Restart",command=lambda: self.closewindow())
		self.closebutton.pack(side="top")
	def callback(self):
	
		global time
		global voltage
		global maxNa
		maxNa=float(self.eNa.get())
		
		global maxK
		maxK=float(self.eK.get())
		
		global maxLeak
		maxLeak=float(self.eLeak.get())
		
		global NaRev
		NaRev=float(self.eNaRev.get())

		global KRev
		KRev=float(self.eKRev.get())

		global LeakRev
		LeakRev=float(self.eLeakRev.get())

		global injcurrent1
		injcurrent1=float(self.eCurrent.get())

		global delay1
		delay1=float(self.edelay1.get())

		global injcurrent2
		injcurrent2=float(self.eCurrent2.get())
		global delay2
		delay1=float(self.edelay2.get())

		legtext='Na('+str(maxNa)+','+str(NaRev)+') '+'K('+str(maxK)+','+str(KRev)+') '+'Leak('+str(maxLeak)+','+str(LeakRev)+')'



		time,voltage=runsimulation(legtext,injcurrent1,injcurrent2,dur1,dur2,delay1,delay2)
		
	def setdefaults(self):
		self.eNa.delete(0,'end')
		self.eNa.insert(0,.12)
		self.eK.delete(0,'end')
		self.eK.insert(0,.036)
		self.eLeak.delete(0,'end')
		self.eLeak.insert(0,.0003)
		self.eNaRev.delete(0,'end')
		self.eNaRev.insert(0,50)
		self.eKRev.delete(0,'end')
		self.eKRev.insert(0,-77)
		self.eLeakRev.delete(0,'end')
		self.eLeakRev.insert(0,-54.3)
		self.eCurrent.delete(0,'end')
		self.eCurrent.insert(0,.1)
	def closewindow(self):
		plt.close()
		global legendlist
		legendlist=list()
		
		




app=ui_window()
app.mainloop()

	


