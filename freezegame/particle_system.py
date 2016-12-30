import random


class ParticleSystem:
    def __init__(self, batch, group):
        self.particles = []
        self.batch = batch
        self.group=group
        
    def update(self, dt, keys, state):
        new_particles = []
        for particle in self.particles:
            particle.update(dt, keys, state)
            if particle.dead is False or particle.keep is True:
                new_particles.append(particle)
            if particle.dead is True:
                particle.on_death()
        self.particles = new_particles
        
    def draw(self):
        self.batch.draw()
    
    def add_particles(self, particle_list, pos, amount):
        for num in range(amount):
            new_particle = random.choice(particle_list)(pos)
            new_particle.batch = self.batch
            self.particles.append(new_particle)
    
    def add_particle(self, particle):
        particle.batch = self.batch
        self.particles.append(particle)
    
    def clear(self):
        self.particles = []
