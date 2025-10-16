"""Run the game."""
import pyglet
import cProfile
import pstats
import dcrawls as dc
from dcrawls import ui
import io


world = dc.Encounter()
p1 = world.add_character()[0]
p2 = world.add_character()[0]
# TODO: make setting both with list doable - test and implement
world.loc[[p1, p2], dc.position] = [[25, 50], [25, 50]]
world.loc[[p1, p2], dc.size] = [10, 15]
world.loc[[p1, p2], dc.run_acceleration] = [900, 500]

game = ui.GameWindow(world)
world.add_enemy()
s = io.StringIO()
pr = cProfile.Profile()
pr.enable()

pyglet.app.run()

pr.disable()

pr.dump_stats("gameplay.prof")

ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()
with open('stats.tsv', 'w+') as f:
    f.write(s.getvalue())
    
import pandas as pd
stats = pd.read_csv("stats.tsv", sep='\t')




