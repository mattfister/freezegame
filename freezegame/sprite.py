import copy
import pyglet
import pyglet.sprite

from pyglet.sprite import *
from freezegame import resources
from freezegame.animation import Animation
from freezegame.rect import Rect


class Sprite:
    def __init__(self, x, y, box, state, image_name=None, image_region=None, batch=None, group=None):
        self.x = x
        self.y = y

        self.on_ground = False
        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.deadly_to_player = False
        self.deadly_to_enemies = False
        self.tileable = True
        self.on = False
        self.invincible = False
        self.frictional = True
        self.updatable = True
        self.enemy = False

        # box is defined [rel_lower_x, rel_lower_y, width, height]
        # it is relative to self.x and self.y
        self.boundingBox = box
        self.box = copy.copy(box)

        # used for rabbyt rdc (32 cause our x and y aren't centered like rabbyt expects)
        self.bounding_radius = 32

        self.vx = 0
        self.vy = 0

        self.state = state

        self.physical_to_sprites = True  # Interact during collisions
        self.physical_to_walls = True
        self.sensor_for_sprites = True
        self.sensor_for_walls = True
        self.gravitic = True  # Is moved by gravity 
        self.fixed = False  # Is moved when colliding with other sprites
        self.tile = False

        self.image_name = image_name
        self.image_region = image_region

        self.sprite = None
        self.batch = batch
        self.group = group

        self.absolute_scale = 1.0

        self.set_sprite(image_name, image_region, batch, group)

        self.last_set_color = [0, 0, 0]
        self.color = [0, 0, 0]  # blend color 0-255, use accessors to set

        self.dead = False
        self.collected = False

        self.desired_position = [self.x, self.y]

        self.animations = {}
        self.cur_animation = None

        self.max_v_x = self.state.maxVX
        self.max_v_y = self.state.maxVYPlus
        self.max_v_y_minus = self.state.maxVYMinus

        self.vision_cone_r = 32 * 20.0

    def add_animation(self, name, frames, loops=True, fps=30.0):
        self.animations[name] = Animation(self, name, frames, loops, fps)

    def create_animations(self):
        pass

    def remove_animations(self):
        self.animations = {}
        self.cur_animation = None

    def play_animation(self, name):
        if self.cur_animation is not None:
            if self.cur_animation.loops:
                if self.cur_animation.playing is True and self.cur_animation.name == name:
                    return
        if self.cur_animation is not None:
            self.cur_animation.stop()
        if name in self.animations.keys():
            self.cur_animation = self.animations[name]
            self.cur_animation.play()

    def get_current_rect(self):
        box = Rect(self.box[0] + self.x, self.box[1] + self.y, self.box[2], self.box[3])
        return box

    def get_collision_rect(self):
        box = Rect(self.box[0] + self.desired_position[0], self.box[1] + self.desired_position[1], self.box[2],
                   self.box[3])
        return box

    def get_collision_rect_x(self):
        box = Rect(self.box[0] + self.desired_position[0], self.box[1] + self.y, self.box[2], self.box[3])
        return box

    def get_collision_rect_y(self):
        box = Rect(self.box[0] + self.x, self.box[1] + self.desired_position[1], self.box[2], self.box[3])
        return box

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_pos(self):
        return [self.x, self.y]

    def get_screen_pos(self):
        return [self.get_screen_x(), self.get_screen_y()]

    def get_screen_x(self):
        return self.x

    def get_screen_y(self):
        return self.y

    def get_speed(self):
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)

    def prep_for_pickle(self):
        self.sprite = None
        self.batch = None
        self.group = None
        self.remove_animations()

    def restore_from_pickle(self, state, group):
        self.state = state
        self.batch = self.state.batch
        self.group = group
        self.set_sprite(self.image_name, self.image_region, self.batch, self.group)
        self.create_animations()

    def set_sprite(self, image_name=None, image_region=None, batch=None, group=None):
        self.image_name = image_name
        self.image_region = copy.copy(image_region)
        if self.image_name is not None:
            if self.image_region is None:
                self.sprite = pyglet.sprite.Sprite(resources.images.__dict__[self.image_name], self.x, self.y,
                                                   batch=batch, group=group)
            else:
                self.sprite = pyglet.sprite.Sprite(resources.images.__dict__[self.image_name].get_region(*image_region),
                                                   self.x, self.y, batch=batch, group=group)

        if self.sprite is not None:
            # self.sprite.image.anchor_x = image_region[2]/2
            # self.sprite.image.anchor_y = image_region[3]/2
            self.sprite.x = self.x
            self.sprite.y = self.y

    def set_animation_sprite(self, animation_sprite):
        self.sprite.delete()
        self.sprite = None
        self.sprite = pyglet.sprite.Sprite(animation_sprite, self.x, self.y, batch=self.batch, group=self.group)

    def set_color(self, new_color):
        self.color = new_color
        if self.sprite is not None:
            self.sprite.color = self.color
        self.last_set_color = copy.copy(self.color)

    def draw(self):
        self.sprite.draw()

    def update_sprite_pos(self):
        self.sprite.x = self.x  # - self.boundingBox[0]
        self.sprite.y = self.y  # - self.boundingBox[1]

    def clamp_v(self):
        if self.vx > self.max_v_x:
            self.vx = self.max_v_x
        elif self.vx < -self.max_v_x:
            self.vx = -self.max_v_x
        if self.vy > self.max_v_y:
            self.vy = self.max_v_y
        elif self.vy < self.max_v_y_minus:
            self.vy = self.max_v_y_minus

    def delete(self):
        self.sprite.delete

    def alert(self):
        pass

    def update(self, dt, keys, state):
        gravity_step = 0.0;

        if self.frictional:
            self.vx -= dt * self.vx * self.state.fric

        self.clamp_v()
        old_y = self.y

        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        if self.gravitic:
            gravity_step = dt * self.state.gravity

        self.vy += gravity_step

        self.desired_position = [new_x, new_y]

        self.update_animations(dt, keys, state)

        if new_y == old_y and self.on_ground:
            self.on_ground = True
        else:
            self.on_ground = False

        self.collide_left = False
        self.collide_right = False
        self.collide_top = False

        if self.cur_animation is not None:
            self.cur_animation.update(dt, keys)

    def update_animations(self, dt, keys, state):
        if self.vx > 10:
            self.play_animation('walkRight')
            if not self.on_ground:
                if self.animation_name() != 'jumpRight':
                    self.play_animation('jumpRight')
                elif self.animation_name() == 'walkLeft':
                    self.play_animation('standLeft')
        elif self.vx > 0:
            if self.animation_name() == 'walkRight':
                self.play_animation('standRight')
            elif self.animation_name() == 'walkLeft':
                self.play_animation('standLeft')
        elif self.vx < -10:
            self.play_animation('walkLeft')
            if not self.on_ground:
                if self.animation_name() != 'jumpLeft':
                    self.play_animation('jumpLeft')
                elif self.animation_name() == 'walkLeft':
                    self.play_animation('standLeft')
        else:
            if self.animation_name() == 'walkRight':
                self.play_animation('standRight')
            elif self.animation_name() == 'walkLeft':
                self.play_animation('standLeft')

    def stop_animation(self):
        if self.cur_animation is not None:
            self.cur_animation.stop()

    def animation_name(self):
        if self.cur_animation is not None:
            return self.cur_animation.name
        return None

    def is_dead(self):
        return self.dead

    def die(self):
        self.dead = True

    def distance(self, sprite):
        return math.sqrt((self.x - sprite.x) * (self.x - sprite.x) + (self.y - sprite.y) * (self.y - sprite.y))

    def finish_resolution(self):
        self.x = self.desired_position[0]
        self.y = self.desired_position[1]

    def finish_resolution_x(self):
        self.x = self.desired_position[0]

    def finish_resolution_y(self):
        self.y = self.desired_position[1]

    def resolve_sprite_collision(self, other_sprite, dimension):
        physical = False
        collided = False
        if self.physical_to_sprites and other_sprite.physicalToSprites:
            physical = True

        if self == other_sprite:
            return
        # if self.get_collision_rect().collides(other_sprite.get_collision_rect()):
        if dimension == 'x':
            collision_rect = self.get_collision_rect_x()
        else:
            collision_rect = self.get_collision_rect_y()
        if collision_rect.collides(other_sprite.get_current_rect()):
            collided = True
            intersection = collision_rect.get_intersect(other_sprite.get_current_rect())
            other_rect = other_sprite.get_current_rect()
            del_x = self.desired_position[0] - self.x
            del_y = self.desired_position[1] - self.y

            if dimension == 'x':
                if del_x < 0:
                    if physical:
                        if not self.fixed:
                            self.desired_position = [self.desired_position[0] + intersection.width,
                                                     self.desired_position[1]]
                            self.vx = 0
                        else:
                            other_sprite.x = self.desired_position[0] + intersection.width
                        self.collide_left = True
                        other_sprite.collide_right = True
                elif del_x > 0:
                    if physical:
                        if not self.fixed:
                            self.desired_position = [self.desired_position[0] - intersection.width,
                                                     self.desired_position[1]]
                            self.vx = 0
                        else:
                            other_sprite.x = other_sprite.x - intersection.width
                        self.collide_right = True
                        other_sprite.collide_right = True
            else:
                if del_y < 0:
                    if physical:
                        if not self.fixed:
                            self.desired_position = [self.desired_position[0],
                                                     self.desired_position[1] + intersection.height]
                            self.vy = 0
                        self.on_ground = True
                        other_sprite.collide_top = True
                elif del_y > 0:
                    if physical:
                        if not self.fixed:
                            self.desired_position = [self.desired_position[0],
                                                     self.desired_position[1] - intersection.height]
                            self.vy = 0
                        else:
                            other_sprite.y = other_sprite.y + intersection.height
                        self.collide_top = True
                        other_sprite.collide_ground = True

        if collided:
            if self.sensor_for_sprites:
                self.collision_callback(other_sprite)
            if other_sprite.sensorForSprites:
                other_sprite.collision_callback(self)

    def toggle(self):
        pass

    def collides_point(self, x, y):
        return self.get_collision_rect().collides_point(x, y)

    def collision_callback(self, other_sprite):
        pass

    def on_death(self):
        pass

    def can_see(self, facing_right, other_sprite):
        if other_sprite == None:
            return False
        dx = other_sprite.x - self.x
        if (dx > 0 and not facing_right) or (dx < 0 and facing_right):
            return False
        if self.distance(other_sprite) > self.vision_cone_r:
            return False
        else:
            if self.state.map.get_straight_path([self.x + 16, self.y + 16],
                                                [other_sprite.x + 16, other_sprite.y + 16]) is not None:
                return True
            else:
                return False

    def resolve_tile_map_collisions(self, tile_map):
        tiles = tile_map.get_surrounding_tiles_by_pos([self.x + self.box[0], self.y + self.box[1]])
        for i, tile in enumerate(tiles):
            if tile is not None:
                if self.get_collision_rect().collides(tile.get_collision_rect()):
                    if self.sensor_for_walls:
                        self.collision_callback(tile)
                    if tile.sensor_for_sprites:
                        tile.collision_callback(self)
                    if self.physical_to_walls and tile.physical_to_sprites:
                        intersection = self.get_collision_rect().get_intersect(tile.get_collision_rect())
                        if i == 0:  # Tile is directly below
                            self.desired_position = [self.desired_position[0],
                                                     self.desired_position[1] + intersection.height]
                            self.vy = 0
                            self.on_ground = True
                        elif i == 1:  # Tile is directly above
                            self.desired_position = [self.desired_position[0],
                                                     self.desired_position[1] - intersection.height]
                            self.collide_top = True
                            self.vy = 0
                        elif i == 2:  # Tile is left
                            self.desired_position = [self.desired_position[0] + intersection.width,
                                                     self.desired_position[1]]
                            self.vx = 0
                            self.collide_left = True
                        elif i == 3:  # Tile is right
                            self.desired_position = [self.desired_position[0] - intersection.width,
                                                     self.desired_position[1]]
                            self.vx = 0
                            self.collide_right = True
                        else:
                            if intersection.width > intersection.height:
                                intersection_height = 0
                                if (i > 5):
                                    intersection_height = intersection.height  # might need to flip sign here
                                    self.on_ground = True
                                else:
                                    intersection_height = -intersection.height
                                    self.collide_top = True
                                self.vy = 0
                                self.desired_position = [self.desired_position[0],
                                                         self.desired_position[1] + intersection_height]
                            else:
                                intersection_width = 0
                                if (i == 6 or i == 4):
                                    intersection_width = intersection.width
                                    self.collide_left = True
                                else:
                                    intersection_width = -intersection.width
                                    self.collide_right = True
                                self.vx = 0
                                self.desired_position = [self.desired_position[0] + intersection_width,
                                                         self.desired_position[1]]
