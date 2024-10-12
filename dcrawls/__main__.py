"""Run the game."""
import pyglet

import dcrawls as dc
from dcrawls import ui


world = dc.Encounter()
world.add_entities(
    {
        dc.position.x: 25,
        dc.position.y: 25,
        dc.size: 10,
        dc.velocity.x: 0,
        dc.velocity.y: 0,
        dc.run_acceleration: 900,
        dc.selected: [1],
    }
)
world.add_entities(
    {
        dc.position.x: 50,
        dc.position.y: 40,
        dc.size: 15,
        dc.velocity.x: 0,
        dc.velocity.y: 0,
        dc.run_acceleration: [500],
    }
)

game = ui.GameWindow(world)

pyglet.app.run()
