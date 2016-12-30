from freezegame.sprite import Sprite


class Particle(Sprite):
    def __init__(self, pos, state, image_name, image_region, batch, group, life_time=1.0, vel=[0.0, 0.0],
                 acc=[0.0, 0.0], fric=0.0, rot=0.0, rot_vel=0.0, rot_acc=0.0, rot_fric=0.0, fade=False, fade_in=False):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.fric = fric

        self.rot = rot
        self.rot_vel = rot_vel
        self.rot_acc = rot_acc
        self.rot_fric = rot_fric

        self.life_time = life_time
        self.total_life = self.life_time

        self.dead = False
        self.keep = False

        self.fade = fade
        self.fadeIn = fade_in

        self.max_v = state.maxVX

        Sprite.__init__(self, pos[0], pos[1], [0, 0, 32, 32], state, image_name, image_region, batch, group)
        self.physicalToSprites = False
        self.physicalToWalls = False

        self.sprite.image.anchor_x = image_region[2] / 2  # (self.sprite.width * self.absolute_scale)/2
        self.sprite.image.anchor_y = image_region[3] / 2  # (self.sprite.height * self.absolute_scale)/2

    def update(self, dt, keys, state):
        self.life_time -= dt
        if self.life_time <= 0:
            self.dead = True
            return

        self.vel[0] += self.acc[0] * dt
        self.vel[1] += self.acc[1] * dt

        if self.vel[0] > 0:
            self.vel[0] -= self.fric * dt
            if self.vel[0] < 0:
                self.vel[0] = 0

        if self.vel[0] < 0:
            self.vel[0] += self.fric * dt
            if self.vel[0] > 0:
                self.vel[0] = 0

        if self.vel[1] > 0:
            self.vel[1] -= self.fric * dt
            if self.vel[1] < 0:
                self.vel[1] = 0

        if self.vel[1] < 0:
            self.vel[1] += self.fric * dt
            if self.vel[1] > 0:
                self.vel[1] = 0

        if self.max_v is not None:
            if self.vel[0] > self.max_v:
                self.vel[0] = self.max_v
            if self.vel[0] < -self.max_v:
                self.vel[0] = -self.max_v
            if self.vel[1] > self.max_v:
                self.vel[1] = self.max_v
            if self.vel[1] < -self.max_v:
                self.vel[1] = -self.max_v

        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

        self.rot += self.rot_vel * dt
        self.rot_vel += self.rot_acc * dt

        if self.rot_vel > 0:
            self.rot_vel -= self.rot_fric * dt
            if self.rot_vel < 0:
                self.rot_vel = 0

        if self.rot_vel < 0:
            self.rot_vel += self.rot_fric * dt
            if self.rot_vel > 0:
                self.rot_vel = 0

        if self.fadeIn:
            if self.life_time > self.total_life / 2.0:
                self.sprite.opacity = int(255.0 * (1.0 - float(self.life_time / 2.0) / (float(self.total_life) / 2.0)))

        if self.fade:
            if self.life_time < self.total_life / 2.0:
                self.sprite.opacity = int(255.0 * float(self.life_time / 2.0) / (float(self.total_life) / 2.0))

        self.sprite.rotation = self.rot

        self.x = self.pos[0]
        self.y = self.pos[1]
        self.sprite.x = self.x
        self.sprite.y = self.y

        # PybaconSprite.update(self, dt, keys, state)
