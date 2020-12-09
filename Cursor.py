class Cursor:
    """Class for cursor object"""
    def __init__(self,x=0,y=0):
        self.x,self.y = x,y
        self.sel = -1