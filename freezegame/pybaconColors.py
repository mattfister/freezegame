import random
import copy
import systemSettings
maxColor = 255
minColor = 0

def clampColor(value):
    if value > maxColor:
        return maxColor
    elif value < minColor:
        return minColor
    else:
        return value

def randomDarkColor():
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(0, 100)
    return [r, g, b]

def randomBrightColor():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return [r, g, b]

def randomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]

def randomCloudColor():
    r = g = b = random.randint(222,255)
    return [r, g, b]


def nearbyColor(color):
    newColor = copy.copy(color)
    for i, value in enumerate(newColor):
        value += random.randint(-systemSettings.nearbyColorAmount(), systemSettings.nearbyColorAmount())
        newColor[i] = clampColor(value)
    return newColor

def fartherColor(color):
    newColor = copy.copy(color)
    for i, value in enumerate(newColor):
        value += random.randint(-systemSettings.fartherColorAmount(), systemSettings.fartherColorAmount())
        newColor[i] = clampColor(value)
    return newColor

def inverseColor(color):
    newColor = copy.copy(color)
    for i, value in enumerate(newColor):
        newColor[i] = 255 - color[i];
    return newColor