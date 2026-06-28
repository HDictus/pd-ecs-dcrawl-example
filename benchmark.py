import dcrawls as dc
import numpy as np
import cProfile
import pstats
import io
import pandas as pd
import time


def setup_benchmark(n_enemies=4, n_characters=2):
    encounter = dc.Encounter()
    for _ in range(n_characters):
        encounter.add_character()

    for _ in range(n_enemies):
        encounter.add_enemy()
    return encounter

def run_benchmark(encounter):
    for i in range(200):
        x, y = np.random.randint(900), np.random.randint(500)
        dc.initiate_movement(encounter, x, y)
        encounter.time_passes(0.01)
    return


# times = {}

# for n_enemies in range(0, 1000, 100):
#     start = time.time()
#     run_benchmark(n_enemies=n_enemies, n_characters=n_enemies//4)
#     end = time.time()
#     times[n_enemies] = end - start

# times = pd.Series(times)

enc = setup_benchmark(n_enemies=1000)
pr = cProfile.Profile()
pr.enable()

my_result = run_benchmark(enc)

pr.disable()
pr.dump_stats("benchmark.prof")
# Use snakefviz
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()

with open('stats.tsv', 'w+') as f:
    f.write(s.getvalue().strip())
    

#statsdf = pd.read_csv("stats.tsv", sep='  ', skiprows=[0, 1, 2])
df = pd.DataFrame(
    pr.getstats(),
    columns=['func', 'ncalls', 'ccalls', 'tottime', 'cumtime', 'callers']
)

print(times)
