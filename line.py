class Line:
	def __init__(self, pa, pb, pcanvas, pnum, pcolor="black"):
		self.canv = pcanvas
		self.color = pcolor
		self._num = pnum
		self._a = pa
		self._b = pb
		self.place()

	@property
	def a(self):
		return self._a

	@property
	def b(self):
		return self._b

	@property
	def id(self):
		return self._id

	@property
	def num(self):
		return self._num

	def place(self):
		pt1,pt2 = self.search_points()
		self._id = self.canv.create_line(pt1[0],pt1[1],pt2[0],pt2[1],fill=self.color)
		self.canv.itemconfig(self._id,tags=("line","line_"+str(self._id)))

	def search_points(self):
		x1,y1 = self.unconvert(-20,self._a * (-20) + self._b)
		x2,y2 = self.unconvert(20,self._a * 20 + self._b)
		return([(x1,y1),(x2,y2)])

	def unconvert(self,px,py):
		return(px*20+360, (py*20)*-1+360)

	def delete(self):
		self.canv.delete(self._id)

	def change_color(self, pcolor):
		self.canv.itemconfig(self._id,fill=pcolor)

	def disable(self):
		self.canv.itemconfig(self._id,state='disabled')