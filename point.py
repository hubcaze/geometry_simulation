class Point:

	def __init__(self, pcoords, pcanvas, pnum, pcolor="black"):
		self.canv = pcanvas
		self.color = pcolor
		self._num = pnum
		self._x, self._y = pcoords
		self.place()

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def id(self):
		return self._id

	@property
	def num(self):
		return self._num

	def place(self):
		self._id = self.canv.create_oval(self._x-3,self._y-3,
			self._x+3, self._y+3,fill=self.color, outline=self.color)
		self.canv.itemconfig(self._id,tags=("point","point_"+str(self._id)))

	def delete(self):
		self.canv.delete(self._id)

	def change_color(self, pcolor):
		self.canv.itemconfig(self._id,fill=pcolor, outline=pcolor)

	def disable(self):
		self.canv.itemconfig(self._id,state='disabled')