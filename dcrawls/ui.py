from pd_ecs import System
import dcrawls as dc
import pyglet


class Window:

    def __init__(self, world):
        self.window = pyglet.window.Window(960, 480)
        self.world = world

        @self.window.event
        def on_draw():
            self.world.events.draw(self.window)
            return

        @self.window.event
        def on_mouse_press(x, y, button, mod):
            self.world.events.mouse_pressed(x, y, button)
            return

        @self.window.event
        def on_mouse_release(x, y, button, mod):
            self.world.events.mouse_released(x, y, button)
            return

        @self.window.event
        def update(dt):
            self.world.events.update(dt)
            return

        pyglet.clock.schedule_interval(update, 1/800)


class Render(System):

    filters = dict(
        has_position=[dc.position])

    fps = 0

    def update(self, dt):
        self.fps = 1 / dt

    def draw(self, window):
        window.clear()
        for posn in self.has_position[dc.position].values:
            circle = pyglet.shapes.Circle(
                x=posn[0], y=posn[1],
                radius=10, color=(255, 255, 255))
            circle.draw()
        t = pyglet.text.Label(str(self.fps))
        t.draw()
