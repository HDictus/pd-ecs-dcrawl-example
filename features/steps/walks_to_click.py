import dcrawls as dc
from dcrawls import ui
import numpy as np

def _in_same_direction(vec1, vec2):
    return np.allclose(vec1[dc.X] / vec1[dc.Y], vec2[dc.X] / vec2[dc.Y])

@given(u'the game is in an encounter')
def step_impl(context):
    context.encounter = dc.Encounter()
    context.window = ui.game_window(context.encounter)

@given(u'a character is selected')
def step_impl(context):
    context.selected_character = context.encounter.add_character()
    context.encounter.select_character(context.selected_character)

@when(u'The mouse is clicked at a position')
def step_impl(context):
    x, y  = np.random.randint(960, size=2)
    context.position_pressed = x, y
    context.window.on_mouse_press(x, y)
    context.window.on_mouse_release(x, y)

@then(u'the character should run there with increasing speed')
def step_impl(context):
    current_position = context.encounter[dc.position]\
                              .loc[context.selected_character]
    target_position = context.position_pressed
    diff = target_position - current_position
    distance = np.linalg.norm(diff)
    displacementsize = -1
    while distance > 0:
        context.window.update(0.1)
        new_position = context.encounter[dc.position]\
                              .loc[context.selected_character]
        displacement = new_position - current_position
        new_displacementsize = np.linalg.norm(displacement)
        diff = target_position - new_position
        distance = np.linalg.norm(diff)
        if distance == 0:
            break
        try:
            assert _in_same_direction(displacement, diff)
            assert displacementsize < new_displacementsize, f'{displacementsize} < {new_displacementsize}'
        except AssertionError:
            __import__("pdb").set_trace()

        displacementsize = new_displacementsize
        current_position = new_position



@then(u'the character should stop at that position')
def step_impl(context):
    assert np.allclose(
        context.encounter[dc.position].loc[context.selected_character],
        context.position_pressed)
    return


@given(u'there are characters doing something')
def step_impl(context):
    context.character1 = context.encounter.add_character()[0]
    context.character2 = context.encounter.add_character()[0]
    context.encounter.give(
        [context.character1, context.character2],
        {dc.move_command.x: [1000, 1000], 
         dc.move_command.y: [1000, 1000]})
    context.window.update(0.1)


@when(u'one of these characaters becomes idle')
def step_impl(context):
    context.encounter.take(context.character1, dc.move_command)
    context.window.update(0.1)

@then(u'time should stop')
def step_impl(context):
    context.window.update(0.1)
    assert context.window.time_multiplier < 1


@then(u'the idle character should be selected')
def step_impl(context):
    assert all(context.encounter[dc.selected].index == [context.character1])
