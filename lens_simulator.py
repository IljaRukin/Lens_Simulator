import numpy as np
import tkinter as tk
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

rad2deg = lambda x: x*180/np.pi
deg2rad = lambda x: x*np.pi/180

def CalcAndShow(ax,lensNR,f,L,G0,g0,display,thetas,rayC,objC,imgC):
	g = [0]*lensNR
	b = [0]*lensNR
	G = [0]*lensNR
	B = [0]*lensNR
	LensP = [0]*lensNR
	LensD = [0]*lensNR

	G[0] = G0
	g[0] = g0

	#object/image distances
	for ii in range(lensNR):
	    if ii!=0:
	        G[ii] = B[ii-1]
	        g[ii] = L[ii-1] - b[ii-1]
	        LensP[ii] = LensP[ii-1] + L[ii-1]
	    b[ii] = g[ii]*f[ii]/(g[ii]-f[ii])
	    B[ii] = -G[ii]*b[ii]/g[ii]

	#clear plot
	ax.clear()
	ax.axhline(y=0, color='black', linestyle=':')
	ax.axis('off')

	#rays and images
	for theta in thetas:
	    for ii in range(lensNR):
	        
	        G_lens = G[ii]+g[ii]*np.tan(theta)
	        LensD[ii] = max(LensD[ii],abs(G_lens))
	        if display[ii]==1:
	            ax.vlines(LensP[ii]-g[ii],0,G[ii],color=objC)
	            ax.plot([LensP[ii]-g[ii],LensP[ii]],[G[ii],G_lens],color=rayC,linewidth=1)
	        
	        theta = -np.arctan((G[ii]*(1+b[ii]/g[ii])+g[ii]*np.tan(theta))/b[ii])
	        #B[ii] = G_lens+b[ii]*np.tan(theta)
	        if display[ii+1]==1:
	            ax.vlines(LensP[ii]+b[ii],0,B[ii],color=imgC)
	            ax.plot([LensP[ii],LensP[ii]+b[ii]],[G_lens,B[ii]],color=rayC,linewidth=1)
	        else:
	            ax.plot([LensP[ii],LensP[ii+1]],[G_lens,G_lens+L[ii]*np.tan(theta)],color=rayC,linewidth=1)

	#lenses
	#ax = plt.gca()
	for p,h in zip(LensP,LensD):
	    ellipse = mpl.patches.Ellipse(xy=(p, 0), width=30, height=(h*2)+10)
	    ax.add_patch(ellipse)
	
	canvas.draw()

	#return G,B,g,b,LensP,LensD


def formatData(ax,lensNR,val_f,val_L,val_G0,val_g0,val_display,val_thetas,val_rayC,val_objC,val_imgC):
	g0 = float(val_g0.get())
	G0 = float(val_G0.get())

	val_thetas = val_thetas.get().split(',')
	thetas = np.zeros(len(val_thetas))
	for ii in range(len(val_thetas)):
		thetas[ii] = float(val_thetas[ii])
	thetas = deg2rad(thetas)

	f = [0]*len(val_f)
	for ii in range(len(f)):
		f[ii] = float(val_f[ii].get())

	L = [0]*len(val_L)
	for ii in range(len(L)):
		L[ii] = float(val_L[ii].get())

	display = [0]*len(val_display)
	for ii in range(len(display)):
		display[ii] = int(val_display[ii].get())

	rayC = val_rayC.get()
	objC = val_objC.get()
	imgC = val_imgC.get()

	CalcAndShow(ax,lensNR,f,L,G0,g0,display,thetas,rayC,objC,imgC)


root = tk.Tk()
root.title('Lens Simulator')

fig = Figure(figsize=(8,4),dpi=120)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#--- ask lens number
lensNR = int(tk.simpledialog.askstring(title='set Number of Lenses', prompt='set the number of lenses:'))

#--- object position g0,G0

frame1 = tk.Frame(root)
frame1.pack()

lab_g0 = tk.Label(frame1, text='object distance g0: ')
lab_g0.pack( side = tk.LEFT )

val_g0 = tk.StringVar()
box_g0 = tk.Entry(frame1, width=5, text=val_g0)
val_g0.set(35)
box_g0.pack( side = tk.LEFT )

lab_G0 = tk.Label(frame1, text='object size G0: ')
lab_G0.pack( side = tk.LEFT )

val_G0 = tk.StringVar()
box_G0 = tk.Entry(frame1, width=5, text=val_G0)
val_G0.set(10)
box_G0.pack( side = tk.LEFT )

#--- ray angles

frame5 = tk.Frame(root)
frame5.pack()

lab_thetas = tk.Label(frame5, text='ray angles: ')
lab_thetas.pack( side = tk.LEFT )

val_thetas = tk.StringVar()
box_thetas = tk.Entry(frame5, width=5, text=val_thetas)
val_thetas.set('-5,0,5')
box_thetas.pack( side = tk.LEFT )

#--- focal lenghts f

frame2 = tk.Frame(root)
frame2.pack()

lab_ff = tk.Label(frame2, text='lens focal lenghts: ')
lab_ff.pack( side = tk.LEFT )

val_f = [0]*lensNR
lab_f = [0]*lensNR
box_f = [0]*lensNR
for ii in range(len(val_f)):
	lab_f[ii] = tk.Label(frame2, text='f'+str(ii)+' ')
	lab_f[ii].pack( side = tk.LEFT )

	val_f[ii] = tk.StringVar()
	box_f[ii] = tk.Entry(frame2, width=5, text=val_f[ii])
	val_f[ii].set(50)
	box_f[ii].pack( side = tk.LEFT )

#--- lens spacing L

frame3 = tk.Frame(root)
frame3.pack()

lab_LL = tk.Label(frame3, text='lens spacing: ')
lab_LL.pack( side = tk.LEFT )

val_L = [0]*lensNR
lab_L = [0]*lensNR
box_L = [0]*lensNR
for ii in range(len(val_L)):
	lab_L[ii] = tk.Label(frame3, text='L'+str(ii)+'-L'+str(ii+1)+' ')
	lab_L[ii].pack( side = tk.LEFT )

	val_L[ii] = tk.StringVar()
	box_L[ii] = tk.Entry(frame3, width=5, text=val_L[ii])
	val_L[ii].set(140)
	box_L[ii].pack( side = tk.LEFT )

#--- ray/image colors

frame6 = tk.Frame(root)
frame6.pack()

lab_rayC = tk.Label(frame6, text='ray color: ')
lab_rayC.pack( side = tk.LEFT )

val_rayC = tk.StringVar()
box_rayC = tk.Entry(frame6, width=5, text=val_rayC)
val_rayC.set('orange')
box_rayC.pack( side = tk.LEFT )

lab_objC = tk.Label(frame6, text='object color: ')
lab_objC.pack( side = tk.LEFT )

val_objC = tk.StringVar()
box_objC = tk.Entry(frame6, width=5, text=val_objC)
val_objC.set('green')
box_objC.pack( side = tk.LEFT )

lab_imgC = tk.Label(frame6, text='image color: ')
lab_imgC.pack( side = tk.LEFT )

val_imgC = tk.StringVar()
box_imgC = tk.Entry(frame6, width=5, text=val_imgC)
val_imgC.set('red')
box_imgC.pack( side = tk.LEFT )

#--- displayed images

frame4 = tk.Frame(root)
frame4.pack()

lab_ddisplay = tk.Label(frame4, text='toggle images to display: ')
lab_ddisplay.pack( side = tk.LEFT )

val_display = [0]*(lensNR+1)
box_display = [0]*(lensNR+1)
for ii in range(len(val_display)):
	val_display[ii] = tk.IntVar()
	box_display[ii] = tk.Checkbutton(frame4, text='L'+str(ii), variable=val_display[ii])
	if ii==0 or ii==len(val_display)-1:
		val_display[ii].set(1)
	else:
		val_display[ii].set(0)
	box_display[ii].pack( side = tk.LEFT )

#----- commands: update & save

frame8 = tk.Frame(root)
frame8.pack( side = tk.BOTTOM )

update = tk.Button(frame8, text='update', command = lambda: formatData(ax,lensNR,val_f,val_L,val_G0,val_g0,val_display,val_thetas,val_rayC,val_objC,val_imgC) )
update.pack( side = tk.LEFT )

save = tk.Button(frame8, text='save', command = lambda: fig.savefig('lens_simulation.png') )
save.pack( side = tk.LEFT )


#----- display with default values
formatData(ax,lensNR,val_f,val_L,val_G0,val_g0,val_display,val_thetas,val_rayC,val_objC,val_imgC)

#----- loop tkinter
tk.mainloop()
