import dcrawls as dc
import pyglet


class Window(pyglet.window.Window):
    
    time_multiplier = 1
    
    def on_draw(self):
        self.clear()
        position = self.world[dc.position]
        for posn in position.values: # this can eventually be used to draw sprites and stuff
            circle = pyglet.shapes.Circle(
                x=posn[0], y=posn[1],
                radius=10, color=(255, 255, 255))
            circle.draw()
        t = pyglet.text.Label(str(self.fps))
        t.draw()

    def update(self, dt):
        self.fps = 1 / dt
        if len(self.world[dc.selected]) > 0:
            self.time_multiplier = 0.5
        else:
            self.time_multiplier = 1
        self.world.time_passes(dt * self.time_multiplier)
        
    def on_mouse_press(self, x, y, button=1, mod=None):
        dc.initiate_movement(self.world, x, y)
        
    def on_mouse_release(self, *a, **kw):
        return


def game_window(world):
    window = Window(960, 480)

    window.fps = 0
    window.selected = None
    window.world = world
    pyglet.clock.schedule_interval(window.update, 1/800)
    return window    

