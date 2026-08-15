import dcrawls as dc
import numpy as np

@given(u'a character is walking to a point')
def step_impl(context):
    context.encounter.give(context.player_char1, {dc.move_x: 20, dc.move_y: 20})
    context.moving_character = context.player_char1

@when(u'the character arrives')
def step_impl(context):
    while context.moving_character in context.encounter[dc.move_x].index:
        context.window.update(0.01)

@then(u'the character swings their weapon')
def step_impl(context):
    context.encounter.loc[context.moving_character, dc.attack_angle]


@given(u'one of them is swinging their weapon')
def step_impl(context):
    context.attacking_character = context.player_char1
    dc.character_attacks(
        context.encounter,
        context.attacking_character,
        0
    )
    context.encounter.attack_angle = 0


def _attack_in_contact(world, character, enemy):
    attack_ang, dist = world.loc[character, [dc.attack_angle, dc.attack_dist]]
    diff = world.loc[character, [dc.position_x, dc.position_y]] - world.loc[enemy, [dc.position_x, dc.position_y]]
    p_dist = np.linalg.norm(diff)
    angled_twd = np.abs(attack_ang - np.arctan2(diff.iloc[1], diff.iloc[0])) < 5
    return p_dist <= dist and angled_twd


@when(u'the weapon makes contact with an enemy')
def step_impl(context):
    context.prev_health = context.encounter.loc[context.enemy, dc.current_health]
    posn = context.encounter.loc[context.attacking_character, [dc.position_x, dc.position_y]]
    context.encounter.loc[context.enemy, [dc.position_x, dc.position_y]] = posn.values + np.array([40, 0])
    while not _attack_in_contact(context.encounter, context.attacking_character, context.enemy):
        context.window.update(0.1)


@then(u'the enemy should take damage')
def step_impl(context):
    assert context.encounter.loc[context.enemy, dc.current_health] < context.prev_health
