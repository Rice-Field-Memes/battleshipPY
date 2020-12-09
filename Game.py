import pyglet

grid_offx, grid_offy = 96,48

coordP = lambda xy : (xy[0]*64+grid_offx, xy[1]*64+grid_offy)
coordX = lambda x : x*64+grid_offx
coordY = lambda y : y*64+grid_offy

hit1 = pyglet.resource.image('images/1hit_or.png')
hit1.anchor_x,hit1.anchor_y=32,32

miss1 = pyglet.resource.image('images/1miss_or.png')
miss1.anchor_x,miss1.anchor_y=32,32

info1_place = pyglet.resource.image('images/1info_place.png')
info1_yt = pyglet.resource.image('images/1info_yourturn.png')
info1_et = pyglet.resource.image('images/1info_enemturn.png')


class Game(object):
    """class created to hold date about events in game"""
    def __init__(self):
        self.state = 0 #0: placing ships, 1: in game
        self.turn = 0 #turn number
        self.debug = False
        self.infoPlaceSprite = pyglet.sprite.Sprite(info1_place,784,400)
        self.infoYtSprite = pyglet.sprite.Sprite(info1_yt,784,400)
        self.infoEtSprite = pyglet.sprite.Sprite(info1_et,784,400)

        self.occupied = [[0 for _ in range(10)] for _ in range(10)] # 0: not occupied, 1: occupied
        self.shots = [[0 for _ in range(10)] for _ in range(10)] # 0: not hit, 1: missed, 2: hit
        
        self.shotSprites = []
        self.shotBatch = pyglet.graphics.Batch()
        
    def shoot(self,x,y):
        if self.occupied[x][y]==1:
            self.shots[x][y] = 1
            self.shotSprites.append(pyglet.sprite.Sprite(hit1,coordX(x),coordY(y),batch=self.shotBatch))
        else:
            self.shots[x][y] = 2
            self.shotSprites.append(pyglet.sprite.Sprite(miss1,coordX(x),coordY(y),batch=self.shotBatch))

    def setGrid(self,ships):
        """Called when preparation ends, to set up grid. Parameter is ships list"""
        for x,y in [x for x in [e.gCoords() for e in ships] for x in x]:
            self.occupied[x][y] = 1
        print(self.occupied)