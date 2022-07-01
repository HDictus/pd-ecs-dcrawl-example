import dcrawls as dc
import numpy as np

def _in_same_direction(vec1, vec2):
    return np.allclose(vec1[dc.X] / vec1[dc.Y], vec2[dc.X] / vec1[dc.Y])

@given(u'the game is in an encounter')
def step_impl(context):
    context.encounter = dc.Encounter()

@given(u'a character is selected')
def step_impl(context):
    context.selected_character = context.encounter.add_character()
    context.encounter.events.select_character(context.selected_character)

@when(u'The mouse is clicked at a position')
def step_impl(context):
    x, y  = np.random.randint(960, size=2)
    context.position_pressed = x, y
    context.encounter.events.mouse_pressed(x, y)
    context.encounter.events.mouse_released(x, y)

@then(u'the character should run there with increasing speed')
def step_impl(context):
    current_position = context.encounter[dc.position]\
                              .loc[context.selected_character]
    target_position = context.position_pressed
    diff = target_position - current_position
    distance = np.linalg.norm(diff)
    displacementsize = 0
    while distance > 0:
        context.encounter.events.update(0.1)
        new_position = context.encounter[dc.position]\
                              .loc[context.selected_character]
        displacement = new_position - current_position
        new_displacementsize = np.linalg.norm(displacement)
        assert _in_same_direction(displacement, diff)
        assert displacmentsize < new_displacementsize
        displacementsize = new_displacementsize
        current_position = new_position
        diff = target_position - current_position
        distance = np.linalg.norm(diff)


@then(u'the character should stop at that position')
def step_impl(context):
    assert context.encounter[dc.position]\
                  .loc[context.selected_character] ==\
                  context.position_pressed
    return


@given(u'there are characters doing something')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given there are characters doing something')


@when(u'one of these characaters becomes idle')
def step_impl(context):
    raise NotImplementedError(u'STEP: When one of these characaters becomes idle')


@then(u'time should stop')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then time should stop')


@then(u'the idle character should be selected')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the idle character')
