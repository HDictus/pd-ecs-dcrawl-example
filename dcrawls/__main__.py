"""Run the game."""
import pyglet

import dcrawls as dc
from dcrawls import ui


world = dc.Encounter()
world.add_entities(
    {
        dc.position.x: 25,
        dc.position.y: 25,
        dc.velocity.x: 0,
        dc.velocity.y: 0,
        dc.run_acceleration: 900,
        dc.selected: [1],
    }
)

game = ui.GameWindow(world)

pyglet.app.run()
