import dcrawls as dc
import numpy as np
import pytest as pyt


def test_selected_units_are_commanded_to_move():
    world = dc.World()

    selected = world.add_entities(
        {
            dc.position_x: [10, 20, 30],
            dc.position_y: [30, 40, 50],
            dc.velocity_x: 0,
            dc.velocity_y: 0,
            dc.run_acceleration: 10,
            dc.selected: 1,
        }
    )

    world.add_entities(
        {
            dc.position_x: [10, 20, 30],
            dc.position_y: [30, 40, 50],
            dc.velocity_x: 0,
            dc.velocity_y: 0,
            dc.run_acceleration: 10,
        }
    )

    dc.initiate_movement(world, 400, 500)
    assert set(world[dc.move_x].index) == set(selected)
    assert all(world[dc.move_x] == 400)
    assert all(world[dc.move_y] == 500)


def test_moving_units_accelerate_and_increment_by_vel():

    world = dc.World()

    moving = world.add_entities(
        {
            dc.position_x: [0, 10],
            dc.position_y: [0, 10],
            dc.velocity_x: [0, 10],
            dc.velocity_y: [0, -10],
            dc.run_acceleration: np.sqrt(200),
            dc.move_x: [100, 100],
            dc.move_y: [100, 100],
        }
    )

    dc.move(world, 1)
    # TODO: this sort of works but error is about 0.5
    assert np.allclose(
        world[[dc.velocity_x, dc.velocity_y]].loc[moving].values, [[10, 10], [20, 0]], atol=0.5
    )
    assert np.allclose(
        world[[dc.position_x, dc.position_y]].loc[moving].values, [[10, 10], [30, 10]], atol=0.5
    )


def test_moving_units_stop_when_target_is_reached():
    world = dc.World()

    moving = world.add_entities(
        {
            dc.position_x: [0, 80],
            dc.position_y: [0, 80],
            dc.velocity_x: [20, 20],
            dc.velocity_y: [20, 20],
            dc.run_acceleration: np.sqrt(200),
            dc.move_x: [101, 101],
            dc.move_y: [101, 101],
        }
    )

    for _ in range(50):
        dc.move(world, 0.01)
    assert len(world[dc.move_x]) == 2
    for _ in range(50):
        dc.move(world, 0.01)
    assert moving[1] not in world[dc.move_x].index
    assert np.allclose(world[[dc.position_x, dc.position_y]].loc[moving[1]].values, [101, 101])


def test_select_one_idle():
    world = dc.Encounter()
    movers = world.add_entities(
        {
            dc.position_x: [0, 80],
            dc.position_y: [0, 80],
            dc.velocity_x: [20, 20],
            dc.velocity_y: [20, 20],
            dc.player: True,
            dc.run_acceleration: np.sqrt(200),
            dc.move_x: [1, 1],
            dc.move_y: [2, 2]
        }
    )
    non_player = world.add_entities({
            dc.position_x: [0, 80],
            dc.position_y: [0, 80],
            dc.velocity_x: [20, 20],
            dc.velocity_y: [20, 20],
            dc.run_acceleration: np.sqrt(200)
    })
    dc.select_idle(world)
    assert len(world[dc.selected]) == 0
    world.take(movers, dc.move_x, dc.move_y)
    dc.select_idle(world)
    assert all(world[dc.selected].index == [0])
    dc.select_idle(world)
    assert all(world[dc.selected].index == [0])
    dc.initiate_movement(world, 100, 1232)
    dc.select_idle(world)
    assert all(world[dc.selected].index == [1])
    dc.initiate_movement(world, 100, 1232)
    dc.select_idle(world)
    assert len(world[dc.selected].index) == 0
