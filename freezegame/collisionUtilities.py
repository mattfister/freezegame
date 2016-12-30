def isHorizontalCollision(r1, r2):
    r1Left = r1[0]
    r2Left = r2[0]
    r1Right = r1Left + r1[2]
    r2Right = r2Left + r2[2]
    if r1Left < r2Left and r2Left < r1Right:
        return True
    if r1Left < r2Right and r2Right < r1Right:
        return True
    return False

def isVerticalCollision(r1, r2):
    r1Bottom = r1[1]
    r2Bottom = r2[1]
    r1Top = r1Bottom + r1[3]
    r2Top = r2Bottom + r2[3]
    if r1Bottom < r2Bottom and r2Bottom < r1Top:
        return True
    if r1Bottom < r2Top and r2Top < r1Top:
        return True
    return False

def isContainsCollision(r1, r2):
    r1Left = r1[0]
    r2Left = r2[0]
    r1Right = r1Left + r1[2]
    r2Right = r2Left + r2[2]
    r1Bottom = r1[1]
    r2Bottom = r2[1]
    r1Top = r1Bottom + r1[3]
    r2Top = r2Bottom + r2[3]
    
    if r2Left < r1Left and r1Left < r2Right and r2Bottom < r1Bottom and r1Bottom < r2Top:
        return True
    return False
    
def collideRects(r1, r2):
    if isVerticalCollision(r1, r2) or isHorizontalCollision(r1, r2) or isContainsCollision(r1, r2):
        return True
    return False

 