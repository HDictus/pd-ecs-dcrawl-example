import dcrawls as dc
import numpy as np
import cProfile
import pstats
import io

def run_benchmark():
    encounter = dc.Encounter()
    encounter.add_character()
    encounter.add_character()
    encounter.add_enemy()
    encounter.add_enemy()
    encounter.add_enemy()
    encounter.add_enemy()
    for i in range(100):
        x, y = np.random.randint(900), np.random.randint(500)
        dc.initiate_movement(encounter, x, y)
        encounter.time_passes(0.01)
    return


pr = cProfile.Profile()
pr.enable()

my_result = run_benchmark()

pr.disable()
pr.dump_stats("prof.prof")
# Use snakefviz
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()

with open('stats.tsv', 'w+') as f:
    f.write(s.getvalue())
    
import pandas as pd
pd.read_csv("stats.tsv", )