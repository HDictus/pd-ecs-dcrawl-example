import dcrawls.ui as ui
import dcrawls as dc
import pyglet

import cProfile

# TODO: some bug, seems to snap to destination too soon
world = dc.Encounter()
world.add_entities({
    dc.position.x: 25, dc.position.y: 25,
    dc.velocity.x: 0, dc.velocity.y: 0,
    dc.run_acceleration: 900,
    dc.selected: [1]})
print(world[dc.position][dc.X].dtype)
game = ui.game_window(world)

pyglet.app.run()
