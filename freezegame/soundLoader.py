import pyglet
import os
import random
import systemSettings
import copy

beatCounter = [0,0,0,0]

class SoundLoader(object):
    def __init__(self):
        self.players = []
        for file in os.listdir('./sounds'):
            name = file.split('.')[0]
            self.__dict__[name] = []
            for i in range(len(systemSettings.allNotes)):
                sound = pyglet.media.StaticSource(pyglet.resource.media(file, streaming=False))
                self.__dict__[name].append(pyglet.resource.media(file, streaming=False))
                player = pyglet.media.Player()
                #player.pitch = notes[i]
                player.queue(sound)
            
    
    def reload(self):
        self.__dict__ = {}
        for file in os.listdir('./sounds'):
            name = file.split('.')[0]
            self.__dict__[name] = pyglet.resource.media(file, streaming=False)
    
    def loop(self, sound, volume=1.0):
        name = sound + '_loop'
        self.__dict__[sound] = pyglet.media.Player()
        self.name = self.__dict__[name]
        self.name.queue(self.__dict__[sound])
        self.name.eos_action = 'loop'
        self.name.volume = volume
        self.name.play()
    
    def play(self, sound,  beat=0, volume=1.0):
        if not systemSettings.mute:
            
            self.cleanPlayers()
            
            player = pyglet.media.Player();
            sounds = self.__dict__[sound];
            pitchi = random.randint(0,len(systemSettings.allNotes)-1)
            if beat == 0:
                player.pitch = systemSettings.allNotes[pitchi]
            else:
                currentBeat = copy.copy(beatCounter[beat-1])
                melody = systemSettings.notes[beat-1];
                currentBeat = currentBeat % len(melody)
                
                
                player.pitch = melody[currentBeat]
                if random.randint(1,32) == 1:
                    player.pitch = player.pitch*2;
                beatCounter[beat-1] += 1
            player.queue(copy.copy(sounds[pitchi]));
            player.play();
            self.players.append(player)
            
    def cleanPlayers(self):
        newPlayers = []
        for player in self.players:
            if player.source != None:
                if player.time <= player.source.duration:
                
                    newPlayers.append(player)
            else:
                player.pause()
                
        self.players = newPlayers
        #self.__dict__[sound].pitch = random.random();
        #self.__dict__[sound].play();
    