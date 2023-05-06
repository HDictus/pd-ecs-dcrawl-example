import dcrawls as dc
import numpy as np
import pytest as pyt


def test_selected_units_are_commanded_to_move():
    world = dc.World()

    selected = world.add_entities(
        {dc.position: {dc.X: [10, 20, 30], dc.Y: [30, 40, 50]},
         dc.velocity: {dc.X: 0, dc.Y: 0},
         dc.run_acceleration: {dc.ACCEL: 10},
         dc.selected: {dc.BY: 1}})

    world.add_entities(
        {dc.position: {dc.X: [10, 20, 30], dc.Y: [30, 40, 50]},
         dc.velocity: {dc.X: 0, dc.Y: 0},
         dc.run_acceleration: {dc.ACCEL: 10}})

    dc.initiate_movement(world, 400, 500)
    commanded = world[dc.move_command]
    assert set(commanded.index) == set(selected)
    assert all(commanded[dc.X] == 400)
    assert all(commanded[dc.Y] == 500)


def test_moving_units_accelerate_and_increment_by_vel():

    world = dc.World()

    moving  = world.add_entities(
        {dc.position: {dc.X: [0, 0], dc.Y: [10, 10]},
         dc.velocity: {dc.X: [0, 10], dc.Y: [0, -10]},
         dc.run_acceleration: {dc.ACCEL: np.sqrt(200)},
         dc.move_command: {dc.X: [100, 100], dc.Y: [100, 100]}})

    dc.move(world, 1)
    # TODO: this sort of works but error is about 0.5
    assert np.allclose(
        world[dc.velocity].loc[moving].values,
        [[10, 10],
         [10, 0]])
    assert np.allclose(
        world[dc.position].loc[moving].values,
        [[10, 10],
         [20, 10]])

def test_moving_units_stop_when_target_is_reached():
    world = dc.World()

    moving = world.add_entities(
        {dc.position: {dc.X: [0, 80], dc.Y: [0, 80]},
         dc.velocity: {dc.X: [20, 20], dc.Y: [20, 20]},
         dc.run_acceleration: {dc.ACCEL: np.sqrt(200)},
         dc.move_command: {dc.X: [101, 101], dc.Y: [101, 101]}})

    dc.move(world, 1)

    assert moving[1] not in world[dc.move_command].index
    assert np.allclose(world[dc.position].loc[moving[1]].values,
                       [101, 101])
