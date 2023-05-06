import dcrawls as dc
import pyglet


def game_window(world):
    window = pyglet.window.Window(960, 480)

    window.fps = 0
    window.selected = None


    @window.event
    def on_draw():
        window.clear()
        position = world[dc.position]
        for posn in position.values: # this can eventually be used to draw sprites and stuff
            circle = pyglet.shapes.Circle(
                x=posn[0], y=posn[1],
                radius=10, color=(255, 255, 255))
            circle.draw()
        t = pyglet.text.Label(str(window.fps))
        t.draw()

    @window.event
    def update(dt):
        window.fps = 1 / dt
        dc.move(world, dt)
    pyglet.clock.schedule_interval(update, 1/800)

    @window.event
    def on_mouse_press(x, y, button, mod):
        dc.initiate_movement(world, x, y)

    return window
