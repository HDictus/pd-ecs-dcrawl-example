"""Run the game."""
import pyglet

import dcrawls as dc
from dcrawls import ui


world = dc.Encounter()
p1 = world.add_character()[0]
p2 = world.add_character()[0]
# TODO: make setting both with list doable - test and implement
world.loc[[p1, p2], dc.position] = [[25, 50], [25, 50]]
world.loc[[p1, p2], dc.size] = [10, 15]
world.loc[[p1, p2], dc.run_acceleration] = [900, 500]


world.add_enemy()

game = ui.GameWindow(world)

pyglet.app.run()
