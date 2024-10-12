import dcrawls as dc

@given(u'the player has some characters')
def step_impl(context):
    context.player_char1 = context.encounter.add_character()[0]
    context.player_char2 = context.encounter.add_character()[0]

@given(u'there is an enemy')
def step_impl(context):
    context.enemy = context.encounter.add_enemy()[0]

@when(u'the enemy is idle')
def step_impl(context):
    pass


@then(u'the enemy should move to the nearest player character')
def step_impl(context):
    context.encounter.loc[context.player_char1, dc.position] = [0, 0]
    context.encounter.loc[context.player_char2, dc.position] = [100, 100]
    context.encounter.loc[context.enemy, dc.position] = [51, 51]
    context.window.update(0)
    assert all(context.encounter.loc[context.enemy, dc.move_command] == [100, 100])


@given(u'one of them is touching an enemy')
def step_impl(context):
    context.encounter.loc[context.player_char2, dc.position] = [100, 100]
    context.encounter.loc[context.enemy, dc.position] = [100, 100]


@when(u'time passes')
def step_impl(context):
    health = context.encounter.loc[context.player_char2, dc.health.current]
    context.prev_health = health
    context.dt = 1
    context.window.update(context.dt)


@then(u'the character should take damage')
def step_impl(context):
    health = context.encounter.loc[context.player_char2, dc.health.current]
    assert health < context.prev_health