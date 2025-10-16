import dcrawls as dc
import numpy as np


# TODO: testing dilemma: should I test like this, or more specifically character_attacks and update_attack ?
def test_attack_turns_and_extends():
    """For now, the character's attack both turns and extends and both may reach thei target value at different times."""
    world = dc.Encounter()
    char = world.add_character()[0]
    dc.character_attacks(world, char, np.pi/2)
    dt = 0.1
    world.time_passes(dt)
    assert world.loc[char, dc.angle] == 0 + dt * world.loc[char, dc.turn_speed]
    assert world.loc[char, dc.attack.dist] == world.loc[char, dc.size] + world.loc[char, dc.extend_speed] *  dt

def test_attack_ends_when_angle_reached():
    world = dc.Encounter()
    char = world.add_character()[0]
    dc.character_attacks(world, char, np.pi/2)
    dt = 0.1

    while world.loc[char, dc.angle] < np.pi / 2:
        world.time_passes(dt)
    assert world.loc[char, dc.angle] == np.pi / 2
    assert char not in world[dc.attack].index