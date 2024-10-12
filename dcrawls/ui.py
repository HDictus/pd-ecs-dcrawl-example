"""User interface for the game."""
import pyglet

import dcrawls as dc


# pylint: disable=abstract-method
class GameWindow(pyglet.window.Window):
    """Game window."""

    time_multiplier: float = 1.0
    fps: int = 0
    world: dc.Encounter

    def __init__(self, world):
        super().__init__(960, 480)
        self.selected = None
        self.world = world
        pyglet.clock.schedule_interval(self.update, 1 / 800)

    def on_draw(self):
        """Draw on screen."""
        self.clear()
        radius = 10
        selected = self.world[[dc.position, dc.selected, dc.size]]
        for sel in selected.values:
            circle = pyglet.shapes.Circle(
                x=sel[0], y=sel[1], radius=sel[3] + 2, color=(200, 200, 0)
            )
            circle.draw()
        position = self.world[[dc.position, dc.size]]
        for (
            posn
        ) in position.values:
            circle = pyglet.shapes.Circle(
                x=posn[0], y=posn[1], radius=posn[2], color=(255, 255, 255)
            )
            circle.draw()


        t = pyglet.text.Label(str(self.fps))
        t.draw()

    def update(self, dt):
        """Update world."""
        self.fps = 1 / dt
        if len(self.world[dc.selected]) > 0:
            self.time_multiplier = 0.01
        else:
            self.time_multiplier = 1
        self.world.time_passes(dt * self.time_multiplier)

    # pylint: disable=unused-argument,missing-function-docstring
    def on_mouse_press(self, x, y, button=1, modifiers=None):
        dc.initiate_movement(self.world, x, y)

    # pylint: disable=unused-argument,missing-function-docstring
    def on_mouse_release(self, *a, **kw):
        return
