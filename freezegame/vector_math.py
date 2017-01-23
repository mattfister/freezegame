from math import sqrt


def vector_object_object(a, b):
    return [b.x - a.x, b.y - a.y]


def mag(v):
    return sqrt(v[0]*v[0] + v[1]*v[1])


def norm(v):
    m = mag(v)
    return [v[0]/m, v[1]/m]
