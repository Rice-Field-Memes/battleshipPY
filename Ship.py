import pyglet
class Pos:
    def __init__(self):
        self.x,self.y = 0,0
    def __iter__(self):
        yield self.x
        yield self.y
    def setPos(self, xy):
        self.x = max(min(xy[0],9),0)
        self.y = max(min(xy[1],9),0)
def allCoords(x,y,len,rotate):
    if rotate == 0:
        return [(x,a+1) for a in range(y-len,y)][::-1]
    elif rotate == 1:
        return [(a+1,y) for a in range(x-len,x)][::-1]
    elif rotate == 2:
        return [(x,a) for a in range(y,y+len)]
    elif rotate == 3:
        return [(a,y) for a in range(x,x+len)]
grid_offx, grid_offy = 96,48
coordP = lambda xy : (xy[0]*64+grid_offx, xy[1]*64+grid_offy)
coordX = lambda x : x*64+grid_offx
coordY = lambda y : y*64+grid_offy

class Ship:
    """Class for ship object"""
    def __init__(self,len=3,x=0,y=0):
        self.x, self.y = x,y
        self.gx, self.gy = x,y
        self.len = len
        self.ghost = False
        self.rotate = 3 #0:down, 1:left, 2:up, 3:right
        self.grot = 3
        self.cursOnLine = 0

        self.img = pyglet.resource.image('images/{0}ship.png'.format(self.len))
        self.img.anchor_x,self.img.anchor_y=32,32
        self.sprite = pyglet.sprite.Sprite(img=self.img)
        self.sprite.opacity = 192

        self.ghostImg = pyglet.resource.image('images/{0}ghost.png'.format(self.len))
        self.ghostImg.anchor_x,self.ghostImg.anchor_y=32,32
        self.ghostSprite = pyglet.sprite.Sprite(img=self.ghostImg)
        self.ghostSprite.opacity = 192
    def setPos(self,xy):
        self.x = max(min(xy[0],9),0)
        self.y = max(min(xy[1],9),0)
    def setGP(self,x,y):
        self.gx,self.gy=x,y
    def allCoords(self):
        return allCoords(self.x,self.y,self.len,self.rotate)
    def gCoords(self):
        return allCoords(self.gx,self.gy,self.len,self.grot)
    def update(self):
        self.sprite.update(coordX(self.x),coordY(self.y),rotation=(self.rotate*90+90)%360)
    def updateGhost(self):
        self.ghostSprite.update(coordX(self.gx),coordY(self.gy))
