import random
import pyglet

class PybaconParticleSystem():
    def __init__(self, batch, group):
        self.particles = []
        self.batch = batch
        self.group=group
        
    def update(self, dt, keys, state):
        newParticles = []
        for particle in self.particles:
            particle.update(dt, keys, state)
            if particle.dead == False or particle.keep == True:
                newParticles.append(particle)
            if particle.dead == True:
                particle.onDeath()
        self.particles = newParticles
        
    def draw(self):
        self.batch.draw()
    
    def addParticles(self, particleList, pos, amount):
        for num in range(amount):
            newParticle = random.choice(particleList)(pos)
            newParticle.batch = self.batch
            self.particles.append(newParticle)
    
    def addParticle(self, particle):
        particle.batch = self.batch
        self.particles.append(particle)
    
    def clear(self):
        self.particles = []