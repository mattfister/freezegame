def is_horizontal_collision(r1, r2):
    r1_left = r1[0]
    r2_left = r2[0]
    r1_right = r1_left + r1[2]
    r2_right = r2_left + r2[2]
    if r1_left < r2_left and r2_left < r1_right:
        return True
    if r1_left < r2_right and r2_right < r1_right:
        return True
    return False


def is_vertical_collision(r1, r2):
    r1_bottom = r1[1]
    r2_bottom = r2[1]
    r1_top = r1_bottom + r1[3]
    r2_top = r2_bottom + r2[3]
    if r1_bottom < r2_bottom and r2_bottom < r1_top:
        return True
    if r1_bottom < r2_top and r2_top < r1_top:
        return True
    return False


def is_contains_collision(r1, r2):
    r1_left = r1[0]
    r2_left = r2[0]
    r2_right = r2_left + r2[2]
    r1_bottom = r1[1]
    r2_bottom = r2[1]
    r2_top = r2_bottom + r2[3]

    if r2_left < r1_left and r1_left < r2_right and r2_bottom < r1_bottom and r1_bottom < r2_top:
        return True
    return False


def collide_rects(r1, r2):
    if is_vertical_collision(r1, r2) or is_horizontal_collision(r1, r2) or is_contains_collision(r1, r2):
        return True
    return False
