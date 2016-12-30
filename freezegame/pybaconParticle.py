import math
import copy
import pybaconColors
import random
from   pybacon.pybaconSprite import PybaconSprite

class PybaconParticle(PybaconSprite):
    def __init__(self, pos, state, imageName, imageRegion, batch, group, lifeTime=1.0, vel=[0.0, 0.0], acc=[0.0, 0.0], fric=0.0, rot=0.0, rotVel=0.0, rotAcc=0.0, rotFric=0.0, fade=False, fadeIn=False):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.fric = fric
        
        self.rot = rot
        self.rotVel = rotVel
        self.rotAcc = rotAcc
        self.rotFric = rotFric
        
        self.lifeTime = lifeTime
        self.totalLife = self.lifeTime
        
        
        self.dead = False
        self.keep = False
        
        self.fade = fade
        self.fadeIn = fadeIn
        
        self.maxV = state.maxVX
        
        PybaconSprite.__init__(self, pos[0], pos[1], [0, 0, 32, 32], state, imageName, imageRegion, batch, group)
        self.physicalToSprites = False
        self.physicalToWalls = False
        
        self.sprite.image.anchor_x = imageRegion[2]/2#(self.sprite.width * self.absoluteScale)/2
        self.sprite.image.anchor_y = imageRegion[3]/2#(self.sprite.height * self.absoluteScale)/2        
    
    def update(self, dt, keys, state):
        self.lifeTime -= dt
        if self.lifeTime <= 0:
            self.dead = True
            return
            
        self.vel[0] = self.vel[0] + self.acc[0] * dt
        self.vel[1] = self.vel[1] + self.acc[1] * dt
        
        if self.vel[0] > 0:
            self.vel[0] = self.vel[0] - self.fric * dt
            if self.vel[0] < 0:
                self.vel[0] = 0
        
        if self.vel[0] < 0:
            self.vel[0] = self.vel[0] + self.fric * dt
            if self.vel[0] > 0:
                self.vel[0] = 0
                
        if self.vel[1] > 0:
            self.vel[1] = self.vel[1] - self.fric * dt
            if self.vel[1] < 0:
                self.vel[1] = 0
        
        if self.vel[1] < 0:
            self.vel[1] = self.vel[1] + self.fric * dt
            if self.vel[1] > 0:
                self.vel[1] = 0
        
        if self.maxV != None:
            if self.vel[0] > self.maxV:
                self.vel[0] = self.maxV
            if self.vel[0] < -self.maxV:
                self.vel[0] = -self.maxV
            if self.vel[1] > self.maxV:
                self.vel[1] = self.maxV
            if self.vel[1] < -self.maxV:
                self.vel[1] = -self.maxV
        
        self.pos[0] = self.pos[0] + self.vel[0] * dt
        self.pos[1] = self.pos[1] + self.vel[1] * dt
        
        self.rot = self.rot + self.rotVel * dt
        self.rotVel = self.rotVel + self.rotAcc * dt
        
        if self.rotVel > 0:
            self.rotVel = self.rotVel - self.rotFric * dt
            if self.rotVel < 0:
                self.rotVel = 0
                
        if self.rotVel < 0:
            self.rotVel = self.rotVel + self.rotFric * dt
            if self.rotVel > 0:
                self.rotVel = 0
        
        
        
        if self.fadeIn:
            if self.lifeTime > self.totalLife/2.0:
                self.sprite.opacity = int(255.0*(1.0 - float(self.lifeTime/2.0)/(float(self.totalLife)/2.0)))
        
        if self.fade:
            if self.lifeTime < self.totalLife/2.0:
                self.sprite.opacity = int(255.0*float(self.lifeTime/2.0)/(float(self.totalLife)/2.0))
        
        self.sprite.rotation = self.rot
        
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.sprite.x = self.x
        self.sprite.y = self.y
        
        
        #PybaconSprite.update(self, dt, keys, state)
