import dcrawls.ui as ui
import dcrawls as dc
import pyglet

import cProfile

# TODO: some bug, seems to snap to destination too soon
world = dc.World()
world.add_entities({
    dc.position: {dc.X: 25, dc.Y: 25},
    dc.velocity: {dc.X: 0, dc.Y: 0},
    dc.run_acceleration: {dc.ACCEL: 50},
    dc.selected: {dc.BY: 1}})

game = ui.game_window(world)

pyglet.app.run()
