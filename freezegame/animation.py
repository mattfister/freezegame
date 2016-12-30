import pyglet.image
from pybacon import pybacon_resources


class Animation:
    def __init__(self, sprite, name, frames, loops, fps=30.0):
        self.sprite = sprite
        self.name = name
        self.frames = frames
        self.loops = loops
        self.timeout = 1.0 / fps
        self.timer = self.timeout
        self.curFrame = 0
        self.playing = False

        seq = []
        for frame in self.frames:
            img = pybacon_resources.images.__dict__[self.sprite.image_name].get_region(*frame)
            seq.append(img)

        self.anim = pyglet.image.Animation.from_image_sequence(seq, self.timeout, loops)

    def stop(self):
        self.playing = False

    def update(self, dt, keys):
        pass
        # if (self.playing):
        #    self.timer -= dt
        #    if self.timer <= 0.0:
        #        self.timer = self.timeout
        #        self.curFrame += 1
        #        if self.curFrame >= len(self.frames):
        #            if self.loops:
        #                self.curFrame = 0
        #            else:
        #                self.curFrame -= 1
        #                self.playing = False
        #        self.sprite.setSprite(self.sprite.imageName, self.frames[self.curFrame], self.sprite.batch, self.sprite.group)

    def play(self):
        if self.playing is False or not self.loops:
            self.sprite.setAnimationSprite(self.anim)
            self.playing = True

            # if self.sprite.imageRegion != self.frames[self.curFrame]:
            #    self.sprite.setSprite(self.sprite.imageName, self.frames[self.curFrame], self.sprite.batch, self.sprite.group)

            # self.playing = True
            # if self.loops == False:
            #    self.curFrame = 0
            #    self.timer = self.timeout

    def __str__(self):
        return self.name
