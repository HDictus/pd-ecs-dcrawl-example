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
world.loc[[p1, p2], [dc.position_x, dc.position_y]] = [[100, 400], [125, 450]]
world.loc[[p1, p2], dc.size] = [10, 15]
world.loc[[p1, p2], dc.run_acceleration] = [900, 500]

game = ui.GameWindow(world)
# for i in range(100):
#     world.add_enemy(x=i, y=i*4)
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




