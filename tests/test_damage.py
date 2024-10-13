import dcrawls as dc


def test_damage_in_contact_with_enemy():
    world = dc.Encounter()
    char = world.add_character()
    enemy = world.add_enemy()

    world.loc[enemy, dc.touch_damage] = 10
    world.loc[char, dc.health.current] = 100
    world.loc[char, dc.position] = 0
    world.loc[enemy, dc.position] = 0

    world.time_passes(1)
    assert world.loc[char, dc.health.current].iloc[0] == 90
