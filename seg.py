import math

class Segment:

	def __init__(self, pcoords, pcanvas, pnum, pcolor="black"):
		self.canv = pcanvas
		self.color = pcolor
		self._num = pnum
		self._x, self._y = pcoords
		self._x2 = 0
		self._y2 = 0
		self.place()

	@property
	def len(self):
		x,y = self.convert(self._x,self._y)
		x2,y2 = self.convert(self._x2, self._y2)
		return math.sqrt(pow(x-x2,2)+pow(y-y2,2))

	@property
	def id(self):
		return self._id

	@property
	def num(self):
		return self._num

	def place(self):
		self._id = self.canv.create_line(self._x,self._y,self._x,self._y)
		self.canv.itemconfig(self._id,tags=("seg","seg_"+str(self._id)))

	def delete(self):
		self.canv.delete(self._id)

	def change_color(self, pcolor):
		self.canv.itemconfig(self._id,fill=pcolor)

	def disable(self):
		self.canv.itemconfig(self._id,state='disabled')

	def enable(self):
		self.canv.itemconfig(self._id,state='normal')

	def move(self, pcoords):
		self._x2 = pcoords[0]
		self._y2 = pcoords[1]
		self.canv.coords(self._id,self._x,self._y,pcoords[0],pcoords[1])

	def convert(self, px, py):
		return((px-360)//20,((py-360)*-1)//20)