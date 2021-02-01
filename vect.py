import math

class Vect:

	def __init__(self, pnorm, pangle, pcanvas, pnum, pcolor="black"):
		self.xo = 360
		self.yo = 360
		self.canv = pcanvas
		self.color = pcolor
		self._num = pnum
		self._angle = pangle
		self._norm = pnorm
		self.place()

	@property
	def norm(self):
		return self._norm

	@property
	def angle(self):
		return self._angle

	@property
	def id(self):
		return self._id

	@property
	def num(self):
		return self._num

	def place(self):
		a = math.radians(self._angle)
		self.x,self.y = self.unconvert(self._norm*math.cos(a), self._norm*math.sin(a))
		self._id = self.canv.create_line(360,360,self.x,self.y,arrow="last")
		self.canv.itemconfig(self._id,tags=("vect","vect_"+str(self._id)))

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

	def unconvert(self,px,py):
		return(px*20+360, (py*20)*-1+360)

	def convert(self, px, py):
		return((px-360)/20,((py-360)*-1)/20)

	def rotate(self, pangle):
		angle = math.radians(pangle)
		tmp_x, tmp_y = self.convert(self.x, self.y)
		self.x,self.y= self.unconvert(math.cos(angle)*tmp_x-math.sin(angle)*tmp_y,math.sin(angle)*tmp_x+math.cos(angle)*tmp_y)
		self.canv.coords(self._id,self.xo,self.yo,self.x,self.y)
		self._angle += angle

	def translate(self, dx, dy):
		x,y = self.convert(self.x,self.y)
		new_x,new_y = self.unconvert(x+dx,y+dy)
		self.x = new_x
		self.y = new_y
		self.canv.coords(self._id,self.xo,self.yo,self.x,self.y)

	def scale(self,alpha):
		x,y = self.convert(self.x,self.y)
		new_x,new_y = self.unconvert(x*alpha,y*alpha)
		self.x = new_x
		self.y = new_y
		self.canv.coords(self._id,self.xo,self.yo,self.x,self.y)