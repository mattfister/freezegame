class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def __str__(self):
        return str([self.x, self.y, self.width, self.height])
    
    def as_list(self):
        return [self.x, self.y, self.width, self.height]
    
    def left(self):
        return self.x
    
    def right(self):
        return self.x + self.width
    
    def bottom(self):
        return self.y
    
    def top(self):
        return self.y + self.height
    
    def collides(self, rect2):
        if self.right() <= rect2.left():
            return False
        elif self.left() >= rect2.right():
            return False
        elif self.top() <= rect2.bottom():
            return False
        elif self.bottom() >= rect2.top():
            return False
        else:
            return True
    
    def collides_point(self, x, y):
        if x >= self.left() and x <= self.right() and y >= self.bottom() and y <= self.top():
            return True
        return False
     
    def get_intersect(self, rect2):
        if self.left() > rect2.left() and self.left() < rect2.right():
            left = self.left()
        else:  # rect2.left() > rect.left() and rect2.left() < rect2.right():
            left = rect2.left()
        if self.right() > rect2.left() and self.right() < rect2.right():
            right = self.right()
        else:  # rect2.right() > rect.left() and rect2.left() < rect2.right()
            right = rect2.right()
        
        if self.bottom() > rect2.bottom() and self.bottom() < rect2.top():
            bottom = self.bottom()
        else:  # rect2.bottom() > rect.bottom() and rect2.bottom() < rect2.top():
            bottom = rect2.bottom()
        if self.top() > rect2.bottom() and self.top() < rect2.top():
            top = self.top()
        else:  # rect2.top() > rect.bottom() and rect2.bottom() < rect2.top()
            top = rect2.top()
        
        width = right - left
        height = top - bottom
        return Rect(left, bottom, width, height)     
