import tkinter as tk
import point
import line
import vect
import seg
from tkinter import filedialog, messagebox

class App:

	DICT = {}
	POINTS = []
	SEGS = []
	LINES = []
	VECTS = []
	_nb_points = 0 # number of point in the scene
	_nb_vects = 0 # number of vectors in the scene
	_nb_seg = 0 # number of segments in the scene
	_nb_lines = 0 # number of lines in the scene
	last_select = None

	def __init__(self):

		self.root = tk.Tk()

		self.prev = None
		self.init_scene()

		self.root.mainloop()

	def init_scene(self):

		self.pos = tk.StringVar()

		self.infos = tk.LabelFrame(
			self.root,
			text="Actions")

		self.seg_button = tk.Button(self.infos,
			text="Tracer un segment",command=self.place_seg)
		self.line_button = tk.Button(self.infos,
			text="Tracer une droite",command=self.place_line)
		self.vect_button = tk.Button(self.infos,
			text="Creer un vecteur",command=self.place_vect)
		self.print_infos()

		#infos to create segment
		self.label_seg = tk.Label(self.infos,
			text='Pour tracer un segment, cliquez sur un point, \npuis sur un autre point pour terminer le tracé\n(Clic droit pour annuler)')

		#infos of a point selected
		self.info_point = tk.Label(self.infos,
			textvariable=self.pos)

		self.vect_rotate = tk.Button(self.infos,
			text="Effectuer une rotation",command=self.rotate_vect)

		self.vect_translate = tk.Button(self.infos,
			text="Effectuer une translation",command=self.translate_vect)

		self.vect_scale = tk.Button(self.infos,
			text="Effectuer une homotéthie",command=self.scale_vect)

		self.canv = tk.Canvas(
			self.root,
			width=720,
			height=720,
			bg="white")

		self.root.bind("<Control-z>",self.cancel_point)
		self.canv.bind("<Button-1>",self.place_point)
		self.canv.bind("<Button-3>",self.select)
		self.canv.bind("<Motion>",self.place_point_prev)
		self.draw()

		self.infos.pack(fill="both",side='right')
		self.canv.pack()

	def hide_all(self):
		self.seg_button.pack_forget()
		self.label_seg.pack_forget()
		self.info_point.pack_forget()
		self.vect_button.pack_forget()
		self.line_button.pack_forget()
		self.vect_rotate.pack_forget()
		self.vect_translate.pack_forget()
		self.vect_scale.pack_forget()

	def print_infos(self):
		self.seg_button.pack(pady=20, padx=20)
		self.vect_button.pack(pady=20, padx=20)
		self.line_button.pack(pady=20, padx=20)

	def print_seg_help(self):
		self.label_seg.pack()

	def print_vect_help(self):
		self.info_point.pack(pady=20, padx=20)
		self.vect_rotate.pack(pady=20, padx=20)
		self.vect_translate.pack(pady=20, padx=20)
		self.vect_scale.pack(pady=20, padx=20)

	def print_infos_select(self):
		self.info_point.pack()

	def cancel_point(self, event=None):
		if(len(self.POINTS) > 0):
			pt = self.POINTS.pop()
			self._nb_points -= 1
			pt.delete()

	def select(self, event=None):
		el = self.canv.find_withtag("current")
		tag = self.canv.gettags(el)
		if self.canv.type(el) == "oval":
			point_id = tag[1].split("_")[1]
			pt = self.search_point(point_id)
			pt.change_color("red")
			if(self.last_select != None and self.last_select != pt):
				self.last_select.change_color("black")
			self.last_select = pt
			x,y = self.convert(pt.x,pt.y)
			self.pos.set("Point n° "+str(pt.num)+"\nx : "+str(x)+"\ny : "+str(y))
			self.hide_all()
			self.print_infos_select()
		elif len(tag)>0 and tag[0]=="seg":
			seg_id = tag[1].split("_")[1]
			s = self.search_seg(seg_id)
			s.change_color("red")
			if(self.last_select != None and self.last_select != s):
				self.last_select.change_color("black")
			self.last_select = s
			self.pos.set("Segment n° "+str(s.num)+"\nlongueur : "+str(s.len))
			self.hide_all()
			self.print_infos_select()
		elif len(tag)>0 and tag[0]=="line":
			line_id = tag[1].split("_")[1]
			l = self.search_line(line_id)
			l.change_color("red")
			if(self.last_select != None and self.last_select != l):
				self.last_select.change_color("black")
			self.last_select = l
			self.pos.set("Droite n° "+str(l.num)+"\nEquation: "+str(l.a)+" x + "+str(l.b))
			self.hide_all()
			self.print_infos_select()
		elif len(tag)>0 and tag[0]=="vect":
			vect_id = tag[1].split("_")[1]
			v = self.search_vect(vect_id)
			v.change_color("red")
			if(self.last_select != None and self.last_select != v):
				self.last_select.change_color("black")
			self.last_select = v
			self.pos.set("Vecteur n° "+str(v.num)+"\nNorme: "+str(v.norm)+" Angle: "+str(v.angle)+"°")
			self.hide_all()
			self.print_vect_help()
		else:
			self.hide_all()
			self.print_infos()
			if(self.last_select != None):
				self.last_select.change_color("black")



	# LINES
	def place_line(self):
		self.hide_all()
		self.top = tk.Toplevel()
		lf = tk.LabelFrame(self.top,text="Equation de la droite")
		l = tk.Label(lf, text="coefficient directeur: ")
		self.s = tk.Spinbox(lf, from_=-100, to=100)
		self.s.delete(0, tk.END)
		self.s.insert(0, 0)
		l2 = tk.Label(lf, text="ordonnée à l'origine: ")
		self.s2 = tk.Spinbox(lf, from_=-100, to=100)
		self.s2.delete(0, tk.END)
		self.s2.insert(0, 0)

		b = tk.Button(lf,
			text="Valider",command=self.confirm_line)
		l.grid(column=0, row=0, ipadx=5, pady=5)
		self.s.grid(column=1, row=0, ipadx=5, pady=5)
		l2.grid(column=0, row=1, ipadx=5, pady=5)
		self.s2.grid(column=1, row=1, ipadx=5, pady=5)
		b.grid(column=0, row=2, ipadx=5, pady=5)
		lf.pack(pady=20, padx=20)
		self.print_infos()

	def confirm_line(self):
		a = float(self.s.get())
		b = float(self.s2.get())
		self.top.destroy()
		self._nb_lines += 1
		l = line.Line(a,b,self.canv,self._nb_lines)
		self.LINES.append(l)




	# VECTORS
	def place_vect(self):
		self.hide_all()
		self.top = tk.Toplevel()
		lf = tk.LabelFrame(self.top,text="Paramètres du vecteur")
		l = tk.Label(lf, text="Norme: ")
		self.s = tk.Spinbox(lf, from_=1, to=100)
		self.s.delete(0, tk.END)
		self.s.insert(0, 10)
		l2 = tk.Label(lf, text="Angle (en degrès°): ")
		self.s2 = tk.Spinbox(lf, from_=0, to=360)
		self.s2.delete(0, tk.END)
		self.s2.insert(45, 45)

		b = tk.Button(lf,
			text="Valider",command=self.confirm_vect)
		l.grid(column=0, row=0, ipadx=5, pady=5)
		self.s.grid(column=1, row=0, ipadx=5, pady=5)
		l2.grid(column=0, row=1, ipadx=5, pady=5)
		self.s2.grid(column=1, row=1, ipadx=5, pady=5)
		b.grid(column=0, row=2, ipadx=5, pady=5)
		lf.pack(pady=20, padx=20)
		self.print_infos()

	def confirm_vect(self):
		norm = int(self.s.get())
		angle = int(self.s2.get())
		self.top.destroy()
		self._nb_vects += 1
		v = vect.Vect(norm,angle,self.canv,self._nb_vects)
		self.VECTS.append(v)

	def rotate_vect(self):
		self.hide_all()
		self.top = tk.Toplevel()
		lf = tk.LabelFrame(self.top,text="Paramètres du vecteur")
		l = tk.Label(lf, text="Angle (°degrès): ")
		self.s = tk.Spinbox(lf, from_=1, to=360)
		self.s.delete(0, tk.END)
		self.s.insert(0, 45)

		b = tk.Button(lf,
			text="Valider",command=self.confirm_rotate)
		l.grid(column=0, row=0, ipadx=5, pady=5)
		self.s.grid(column=1, row=0, ipadx=5, pady=5)
		b.grid(column=0, row=1, ipadx=5, pady=5)
		lf.pack(pady=20, padx=20)
		self.print_infos()

	def confirm_rotate(self):
		angle = int(self.s.get())
		self.last_select.rotate(angle)

	def translate_vect(self):
		self.hide_all()
		self.top = tk.Toplevel()
		lf = tk.LabelFrame(self.top,text="Paramètres de translation")
		tk.Label(lf, text="Vecteur v")
		l = tk.Label(lf, text="x: ")
		self.s = tk.Spinbox(lf, from_=1, to=360)
		self.s.delete(0, tk.END)
		self.s.insert(0, 45)
		l2 = tk.Label(lf, text="y: ")
		self.s2 = tk.Spinbox(lf, from_=1, to=360)
		self.s2.delete(0, tk.END)
		self.s2.insert(0, 45)
		b = tk.Button(lf,
			text="Valider",command=self.confirm_translate)
		l.grid(column=0, row=0, ipadx=5, pady=5)
		self.s.grid(column=1, row=0, ipadx=5, pady=5)
		l2.grid(column=0, row=1, ipadx=5, pady=5)
		self.s2.grid(column=1, row=1, ipadx=5, pady=5)
		b.grid(column=0, row=2, ipadx=5, pady=5)
		lf.pack(pady=20, padx=20)
		self.print_infos()

	def confirm_translate(self):
		x = int(self.s.get())
		y = int(self.s2.get())
		self.last_select.translate(x,y)

	def scale_vect(self):
		self.hide_all()
		self.top = tk.Toplevel()
		lf = tk.LabelFrame(self.top,text="Paramètres d'homotéthie")
		l = tk.Label(lf, text="Rapport alpha: ")
		self.s = tk.Spinbox(lf, from_=1, to=360)
		self.s.delete(0, tk.END)
		self.s.insert(0, 0)
		b = tk.Button(lf,
			text="Valider",command=self.confirm_scale)
		l.grid(column=0, row=0, ipadx=5, pady=5)
		self.s.grid(column=1, row=0, ipadx=5, pady=5)
		b.grid(column=0, row=1, ipadx=5, pady=5)
		lf.pack(pady=20, padx=20)
		self.print_infos()

	def confirm_scale(self):
		alpha = float(self.s.get())
		self.last_select.scale(alpha)

	# SEGMENTS
	def place_seg(self):
		if self._nb_points < 2:
			messagebox.showerror(
				title="Error",
				message="Il faut au moins 2 points pour former un segment"
			)
		else:
			self.hide_all()
			self.print_seg_help()
			self.canv.unbind("<Button-3>")
			self.canv.unbind("<Button-1>")
			self.canv.bind("<Button-1>",self.create_seg)

	def cancel_edit_seg(self,event=None):
		self.canv.unbind("<Motion>")
		self.canv.unbind("<Button-1>")
		self.canv.unbind("<Button-3>")
		self.curr_seg.delete()
		self.canv.bind("<Button-1>",self.place_point)
		self.canv.bind("<Button-3>",self.select)
		self.canv.bind("<Motion>",self.place_point_prev)
		self.hide_all()
		self.print_infos()

	def create_seg(self, event):
		point = self.canv.find_withtag("current")
		tag = self.canv.gettags(point)
		if self.canv.type(point) == "oval":
			point_id = tag[1].split("_")[1]
			pt = self.search_point(point_id)
			self.x = pt.x
			self.y = pt.y
			self._nb_seg += 1
			self.curr_seg = seg.Segment((self.x,self.y),self.canv, self._nb_seg)
			self.curr_seg.disable()
			self.canv.unbind("<Motion>")
			self.canv.unbind("<Button-1>")
			self.canv.bind("<Button-3>",self.cancel_edit_seg)
			self.canv.bind("<Motion>", self.move_seg)

	def move_seg(self,event):
		self.curr_seg.move((event.x,event.y))
		self.canv.bind("<Button-1>",self.confirm_seg)

	def confirm_seg(self,event):
		point = self.canv.find_withtag("current")
		tag = self.canv.gettags(point)
		if self.canv.type(point) == "oval":
			point_id = tag[1].split("_")[1]
			pt = self.search_point(point_id)
			self.canv.unbind("<Motion>")
			self.canv.unbind("<Button-1>")
			self.canv.unbind("<Button-3>")
			self.curr_seg.enable()
			self.curr_seg.move((pt.x,pt.y))
			self.canv.bind("<Button-1>",self.place_point)
			self.canv.bind("<Button-3>",self.select)
			self.canv.bind("<Motion>",self.place_point_prev)
			self.raise_point()
			self.hide_all()
			self.print_infos()
			self.SEGS.append(self.curr_seg)

	def search_point(self, pid):
		for point in self.POINTS:
			if point.id == int(pid):
				return point
		return None

	def search_seg(self, pid):
		for seg in self.SEGS:
			if seg.id == int(pid):
				return seg
		return None

	def search_line(self, pid):
		for line in self.LINES:
			if line.id == int(pid):
				return line
		return None

	def search_vect(self, pid):
		for vect in self.VECTS:
			if vect.id == int(pid):
				return vect
		return None


	# POINTS 
	def place_point(self,event):
		coords = self.closest_point((event.x,event.y))
		if self.DICT.get(coords) is None:
			self._nb_points += 1
			self.DICT[coords]=1
			pid = point.Point(coords, self.canv, self._nb_points)
			self.POINTS += [pid]

	def place_point_prev(self,event):
		if(self.prev == None):
			self._coords_prev = self.closest_point((event.x,event.y))
			self.prev = point.Point(self._coords_prev, self.canv,self._nb_points,pcolor="#bfbfbf")
			self.prev.disable()
		else:
			coords = self.closest_point((event.x,event.y))
			if(coords != self._coords_prev):
				delta_x = coords[0] - self._coords_prev[0]
				delta_y = coords[1] - self._coords_prev[1]
				self._coords_prev = coords
				self.canv.move(self.prev.id,delta_x,delta_y)

	def raise_point(self):
		self.canv.tag_raise("point")

	def closest_point(self,pcoords):
		x,y = pcoords
		i = 0
		while(x%20):
			if(i==10):
				while(x%20):
					x-=1
				break
			x+=1
			i+=1
		i=0
		while(y%20):
			if(i==10):
				while(y%20):
					y-=1
				break
			y+=1
			i+=1
		return(x,y)

	def draw(self):
		w = int(self.canv.cget("width"))
		h = int(self.canv.cget("height"))
		k=0
		for i in range(0,w,20):
			if(i != 360):
				self.canv.create_line(i,0,i,h,fill="#bfbfbf")
		for i in range(0,h,20):
			if(i == 360):
				self.canv.create_line(k,i,w,i,width=2)
			else:
				self.canv.create_line(0,i,w,i,fill="#bfbfbf")
		self.canv.create_line(360,0,360,h,width=2)

	def convert(self, px, py):
		return((px-360)//20,((py-360)*-1)//20)

	def unconvert(self,px,py):
		return(px*20+360, (py*20)*-1+360)


App()

exit(0)
