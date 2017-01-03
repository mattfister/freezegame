# This is adapted from http://lab.polygonal.de/2006/11/13/collision-detection-with-recursive-dimensional-clustering/
#
# Copyright (c) 2006 Michael Baczynski http://www.polygonal.de
#
# Permission to use, copy, modify, distribute and sell this software
# and its documentation for any purpose is hereby granted without fee,
# provided that the above copyright notice appear in all copies.
# Michael Baczynski makes no representations about the suitability
# of this software for any purpose.
# It is provided "as is" without express or implied warranty.


SUBDIVISION_THRESHOLD = 10
CONTACT_THRESHOLD = .001


class Boundary:
    def __init__(self, boundary_type, position, sprite):
        self.boundary_type = boundary_type
        self.position = position
        self.sprite = sprite


class RDC:

    def __init__(self):
        self.colliding_groups = []

    def recursive_clustering(self, group, axis1, axis2):
        if axis1 == -1 or len(group) < SUBDIVISION_THRESHOLD:
            self.colliding_groups.append(group)
        else:
            boundaries = self.get_open_close_bounds(group, axis1)
            boundaries.sort(key=lambda x: x.position)

            new_axis1 = axis2
            new_axis2 = -1

            group_subdivided = False

            subgroup = []
            count = 0

            k = len(boundaries)

            for i in range(k):
                b = boundaries[i]
                if b.boundary_type == "open":
                    count += 1
                    subgroup.append(b.sprite)
                else:
                    count -= 1
                    if count == 0:
                        if not i == (k - 1):
                            group_subdivided = True
                        if group_subdivided:
                            if axis1 == 0:
                                new_axis1 = 1
                            elif axis1 == 1:
                                new_axis1 = 0
                        self.recursive_clustering(subgroup, new_axis1, new_axis2)
                        subgroup = []

    def get_open_close_bounds(self, group, axis):
        k = len(group)
        boundaries = []

        if axis == 0:
            for i in range(k):
                o = group[i]
                boundaries.append(Boundary("open", o.x + o.box[2]/2 - o.bounding_radius + CONTACT_THRESHOLD, o))
                boundaries.append(Boundary("close", o.x + o.box[2]/2 + o.bounding_radius - CONTACT_THRESHOLD, o))
        elif axis == 1:
            for i in range(k):
                o = group[i]
                boundaries.append(Boundary("open", o.y + o.box[3]/2 - o.bounding_radius + CONTACT_THRESHOLD, o))
                boundaries.append(Boundary("close", o.y + o.box[3]/2 + o.bounding_radius - CONTACT_THRESHOLD, o))

        return boundaries

