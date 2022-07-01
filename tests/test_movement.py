import dcrawls as dc
import pytest as pyt

def test_informative_error_when_commands_nonwalker():
    world = dc.World(dc.position, dc.velocity, dc.run_acceleration, dc.move_command)
    ms = dc.Movement(world)
    invalid_entity = world.add_entities({dc.position: {dc.X: 1, dc.Y: 2}})
    with pyt.raises(ValueError) as ve:
        ms.move_command(invalid_entity, 32, 2)

    assert 'does not have the component(s): ' in str(ve.value)
    return
