import random
import copy

max_color = 255
min_color = 0
nearby_color_amount = 10
farther_color_amount = 20


def clamp_color(value):
    if value > max_color:
        return max_color
    elif value < min_color:
        return min_color
    else:
        return value


def random_dark_color():
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(0, 100)
    return [r, g, b]


def random_bright_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return [r, g, b]


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]


def random_cloud_color():
    r = g = b = random.randint(222,255)
    return [r, g, b]


def nearby_color(color):
    new_color = copy.copy(color)
    for i, value in enumerate(new_color):
        value += random.randint(-nearby_color_amount, nearby_color_amount)
        new_color[i] = clamp_color(value)
    return new_color


def farther_color(color):
    new_color = copy.copy(color)
    for i, value in enumerate(new_color):
        value += random.randint(-farther_color_amount, farther_color_amount)
        new_color[i] = clamp_color(value)
    return new_color


def inverse_color(color):
    new_color = copy.copy(color)
    for i, value in enumerate(new_color):
        new_color[i] = 255 - color[i]
    return new_color
