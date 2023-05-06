import dcrawls.ui as ui
import dcrawls as dc
import pyglet

import cProfile


world = dc.Encounter()
ui.Render(world)
world.events.select_character(
    world.add_character())
game = ui.Window(world)

pyglet.app.run()
