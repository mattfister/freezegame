class AbstractState:

    def __init__(self):
        self.gravity = -600.0
        self.max_v_y_plus = 1000
        self.max_v_y_minus = -400
        self.max_v_x = 100
        self.friction = 2.1
        
    def update(self, dt, keys):
        pass
    
    def draw(self):
        pass
    
    def handle_mouse_press(self, x, y, button, modifiers):
        pass
    
    def handle_mouse_release(self, x, y, button, modifiers):
        pass
    
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
    
    def handle_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
    
    def handle_mouse_motion(self, x, y, dx, dy):
        pass
