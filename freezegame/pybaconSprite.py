import pyglet
import pyglet.sprite
from pyglet.sprite import *
import pybaconResources
import systemSettings
import copy
import rect
from animation import Animation

class PybaconSprite():
    def __init__(self, x, y, box, state, imageName = None, imageRegion = None, batch = None, group = None):
        self.x = x
        self.y = y
        
        self.onGround = False
        self.collideLeft = False
        self.collideRight = False
        self.collideTop = False
        self.deadlyToVermouth = False
        self.deadlyToEnemies = False
        self.tileable = True
        self.on = False
        self.invincible = False
        self.frictional = True
        self.updatable = True
        self.enemy = False
        
        # box is defined [relLowerX, relLowerY, width, height]
        # it is relative to self.x and self.y
        self.boundingBox = box
        self.box = copy.copy(box)
        
        #used for rabbyt rdc (32 cause our x and y aren't centered like rabbyt expects)
        self.bounding_radius = 32
        
        self.vx = 0
        self.vy = 0
        
        self.state = state

        self.physicalToSprites = True  # Interact during collisions
        self.physicalToWalls = True
        self.sensorForSprites = True
        self.sensorForWalls = True
        self.gravitic = True  # Is moved by gravity 
        self.fixed    = False # Is moved when colliding with other sprites 
        self.tile     = False
        
        self.imageName = imageName
        self.imageRegion = imageRegion
        
        self.sprite = None
        self.batch = batch
        self.group = group
        
        self.absoluteScale = 1.0

        self.setSprite(imageName, imageRegion, batch, group)
        
        self.lastSetColor = [0, 0, 0]
        self.color = [0, 0, 0] # blend color 0-255, use accessors to set
    
        self.dead      = False
        self.collected = False
        
        self.desiredPosition = [self.x, self.y]
        
        self.animations = {}
        self.curAnimation = None
        
        self.maxVX = self.state.maxVX
        self.maxVYPlus = self.state.maxVYPlus
        self.maxVYMinus = self.state.maxVYMinus
        
        self.visionConeR = 32*20.0
        
    def addAnimation(self, name, frames, loops = True, fps=30.0):
        self.animations[name] = Animation(self, name, frames, loops, fps)
    
    def createAnimations(self):
        pass
    
    def removeAnimations(self):
        self.animations = {}
        self.curAnimation = None
    
    def playAnimation(self, name):
        if self.curAnimation != None:
            if self.curAnimation.loops == True:
                if self.curAnimation.playing == True and self.curAnimation.name == name:
                    return
        if self.curAnimation != None:
            self.curAnimation.stop()
        if name in self.animations.keys():
            self.curAnimation = self.animations[name]
            self.curAnimation.play()
    
    def getCurrentRect(self):
        box = rect.Rect(self.box[0] + self.x, self.box[1] + self.y, self.box[2], self.box[3])
        return box
    
    def getCollisionRect(self):
        box = rect.Rect(self.box[0] + self.desiredPosition[0], self.box[1] + self.desiredPosition[1], self.box[2], self.box[3])
        return box
    
    def getCollisionRectX(self):
        box = rect.Rect(self.box[0] + self.desiredPosition[0], self.box[1] + self.y, self.box[2], self.box[3])
        return box
    
    def getCollisionRectY(self):
        box = rect.Rect(self.box[0] + self.x, self.box[1] + self.desiredPosition[1], self.box[2], self.box[3])
        return box
    
    def setX(self, x):
        self.x = x
        
    def setY(self, y):
        self.y = y
    
    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        
    def getPos(self):
        return [self.x, self.y]
    
    def getScreenPos(self):
        return [self.getScreenX(), self.getScreenY()]
    
    def getScreenX(self):
        return self.x
    
    def getScreenY(self):
        return self.y
    
    def getSpeed(self):
        return math.sqrt(self.vx*self.vx+self.vy*self.vy)
    def prepForPickle(self):
        self.sprite = None
        self.batch  = None
        self.group  = None
        self.removeAnimations()
        
    def restoreFromPickle(self, state, group):
        self.state = state
        self.batch = self.state.batch
        self.group = group
        self.setSprite(self.imageName, self.imageRegion, self.batch, self.group)
        self.createAnimations()
        
    def setSprite(self, imageName = None, imageRegion = None, batch=None, group=None):
        self.imageName   = imageName
        self.imageRegion = copy.copy(imageRegion)
        if self.imageName != None:
            if self.imageRegion == None:
                self.sprite = pyglet.sprite.Sprite(pybaconResources.images.__dict__[self.imageName], self.x, self.y, batch=batch, group=group)
            else:
                self.sprite = pyglet.sprite.Sprite(pybaconResources.images.__dict__[self.imageName].get_region(*imageRegion), self.x, self.y, batch=batch, group=group)
        
        if self.sprite != None:
            #self.sprite.image.anchor_x = imageRegion[2]/2
            #self.sprite.image.anchor_y = imageRegion[3]/2
            self.sprite.x = self.x
            self.sprite.y = self.y
    
    def setAnimationSprite(self, animationSprite):
        self.sprite.delete()
        self.sprite = None
        self.sprite = pyglet.sprite.Sprite(animationSprite, self.x, self.y, batch=self.batch, group=self.group)
         
    def setColor(self, newColor):
        self.color = newColor
        if self.sprite != None:
            self.sprite.color = self.color
        self.lastSetColor = copy.copy(self.color)
        
    def draw(self):
        self.sprite.draw();
    
    def updateSpritePos(self):
        self.sprite.x = self.x #- self.boundingBox[0]
        self.sprite.y = self.y #- self.boundingBox[1]
    
    def clampV(self):
        if self.vx > self.maxVX:
            self.vx = self.maxVX
        elif self.vx < -self.maxVX:
            self.vx = -self.maxVX
        if self.vy > self.maxVYPlus:
            self.vy = self.maxVYPlus
        elif self.vy < self.maxVYMinus:
            self.vy = self.maxVYMinus
    
    def delete(self):
        self.sprite.delete  
    
    def alert(self):
        pass
    
    def update(self, dt, keys, state):
        gravityStep = 0.0;

        if self.frictional:
            self.vx -= dt*self.vx*self.state.fric
        
        self.clampV()
        oldY = self.y
        
        newX = self.x + self.vx*dt
        newY = self.y + self.vy*dt 
        
        if self.gravitic:
            gravityStep = dt * self.state.gravity
        
        
        self.vy += gravityStep
        
        self.desiredPosition = [newX, newY]
        
        self.updateAnimations(dt, keys, state)
        
        if newY == oldY and self.onGround:
            self.onGround == True
        else:
            self.onGround     = False
        
        self.collideLeft  = False
        self.collideRight = False
        self.collideTop   = False
        
        if self.curAnimation != None:
            self.curAnimation.update(dt, keys)
    
    def updateAnimations(self, dt, keys, state):
        if self.vx > 10:
            self.playAnimation('walkRight')
            if not self.onGround:
                if self.animationName() != 'jumpRight':
                    self.playAnimation('jumpRight')
                elif self.animationName() == 'walkLeft':
                    self.playAnimation('standLeft')
        elif self.vx > 0:
            if self.animationName() == 'walkRight':
                self.playAnimation('standRight')
            elif self.animationName() == 'walkLeft':
                self.playAnimation('standLeft')
        elif self.vx < -10:
            self.playAnimation('walkLeft')
            if not self.onGround:
                if self.animationName() != 'jumpLeft':
                    self.playAnimation('jumpLeft')
                elif self.animationName() == 'walkLeft':
                    self.playAnimation('standLeft')
        else:
            if self.animationName() == 'walkRight':
                self.playAnimation('standRight')
            elif self.animationName() == 'walkLeft':
                self.playAnimation('standLeft')
                
    def stopAnimation(self):
        if self.curAnimation != None:
            self.curAnimation.stop()
    
    def animationName(self):
        if self.curAnimation != None:
            return self.curAnimation.name
        return None
        
    def isDead(self):
        return self.dead
    
    def die(self):
        self.dead = True
        
    def distance(self, sprite):
        return math.sqrt((self.x - sprite.x)*(self.x - sprite.x) + (self.y - sprite.y)*(self.y - sprite.y))
    
    def finishResolution(self):
        self.x = self.desiredPosition[0]
        self.y = self.desiredPosition[1]
    
    def finishResolutionX(self):
        self.x = self.desiredPosition[0]
    
    def finishResolutionY(self):
        self.y = self.desiredPosition[1]
    
    def resolveSpriteCollision(self, otherSprite, dimension):
        physical = False
        collided = False
        if self.physicalToSprites and otherSprite.physicalToSprites:
            physical = True
            
        if ( self == otherSprite ):
            return
        #if self.getCollisionRect().collides(otherSprite.getCollisionRect()):
        if ( dimension == 'x'):
            collisionRect = self.getCollisionRectX()
        else:
            collisionRect = self.getCollisionRectY()
        if collisionRect.collides(otherSprite.getCurrentRect()):
            collided = True
            intersection = collisionRect.getIntersect(otherSprite.getCurrentRect())
            otherRect = otherSprite.getCurrentRect()
            delX = self.desiredPosition[0] - self.x 
            delY = self.desiredPosition[1] - self.y
            
            if dimension == 'x':
                if delX < 0:
                    if ( physical ):
                        if not self.fixed:
                            self.desiredPosition = [self.desiredPosition[0] + intersection.width, self.desiredPosition[1]]
                            self.vx = 0
                        else:
                            otherSprite.x = self.desiredPosition[0] + intersection.width
                        self.collideLeft = True
                        otherSprite.collideRight = True
                elif delX > 0:
                    if ( physical ):
                        if not self.fixed:
                            self.desiredPosition = [self.desiredPosition[0] - intersection.width, self.desiredPosition[1]]
                            self.vx = 0
                        else:
                            otherSprite.x = otherSprite.x - intersection.width
                        self.collideRight = True
                        otherSprite.collideLeft = True
            else:
                if delY < 0:
                    if ( physical ):
                        if not self.fixed:
                            self.desiredPosition = [self.desiredPosition[0], self.desiredPosition[1] + intersection.height]
                            self.vy = 0
                        self.onGround = True
                        otherSprite.collideTop = True
                elif delY > 0:
                    if ( physical ):
                        if not self.fixed:
                            self.desiredPosition = [self.desiredPosition[0], self.desiredPosition[1] - intersection.height]
                            self.vy = 0
                        else:
                            otherSprite.y = otherSprite.y + intersection.height
                        self.collideTop = True
                        otherSprite.collideGround = True
                        
                        
        if ( collided ):
            if self.sensorForSprites:
                self.collisionCallback(otherSprite)
            if otherSprite.sensorForSprites:
                otherSprite.collisionCallback(self)
    
    def toggle(self):
        pass
    
    def collidesPoint(self, x, y):
        return self.getCollisionRect().collidesPoint(x, y)
    
    def collisionCallback(self, otherSprite):
        pass
    
    def onDeath(self):
        pass
    
    def canSee(self, facingRight, otherSprite):
        if otherSprite == None:
            return False
        dx = otherSprite.x - self.x
        if (dx > 0 and not facingRight) or (dx < 0 and facingRight):
            return False
        if self.distance(otherSprite) > self.visionConeR:
            return False
        else:
            if self.state.map.getStraightPath([self.x+16, self.y+16], [otherSprite.x+16, otherSprite.y+16]) != None:
                return True
            else:
                return False
    
    def resolveTileMapCollisions(self, tileMap):
        tiles = tileMap.getSurroundingTilesByPos([self.x + self.box[0], self.y+self.box[1]])
        for i, tile in enumerate(tiles):
            if tile != None:
                if self.getCollisionRect().collides(tile.getCollisionRect()):
                    if self.sensorForWalls:
                        self.collisionCallback(tile)
                    if tile.sensorForSprites:
                        tile.collisionCallback(self)
                    if self.physicalToWalls and tile.physicalToSprites: 
                        intersection = self.getCollisionRect().getIntersect(tile.getCollisionRect())
                        if ( i == 0 ): #Tile is directly below
                            self.desiredPosition = [self.desiredPosition[0], self.desiredPosition[1] + intersection.height]
                            self.vy = 0
                            self.onGround = True
                        elif ( i == 1 ): # Tile is directly above
                            self.desiredPosition = [self.desiredPosition[0], self.desiredPosition[1] - intersection.height]
                            self.collideTop = True
                            self.vy = 0 
                        elif ( i == 2 ): # Tile is left
                            self.desiredPosition = [self.desiredPosition[0] + intersection.width, self.desiredPosition[1]]
                            self.vx = 0
                            self.collideLeft = True
                        elif ( i == 3 ): # Tile is right
                            self.desiredPosition = [self.desiredPosition[0] - intersection.width, self.desiredPosition[1]]
                            self.vx = 0
                            self.collideRight = True
                        else:
                            if intersection.width > intersection.height:
                                intersectionHeight = 0
                                if ( i > 5 ):
                                    intersectionHeight = intersection.height # might need to flip sign here
                                    self.onGround = True
                                else:
                                    intersectionHeight = -intersection.height
                                    self.collideTop = True
                                self.vy = 0
                                self.desiredPosition = [self.desiredPosition[0], self.desiredPosition[1] + intersectionHeight]
                            else:
                                resolutionWidth = 0
                                if ( i == 6 or i == 4 ):
                                    resolutionWidth = intersection.width
                                    self.collideLeft = True
                                else:
                                    resolutionWidth = -intersection.width
                                    self.collideRight = True
                                self.vx = 0
                                self.desiredPosition = [self.desiredPosition[0] + resolutionWidth, self.desiredPosition[1] ]
