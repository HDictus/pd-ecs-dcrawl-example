import dcrawls as dc
import numpy as np
import pytest as pyt


def test_selected_units_are_commanded_to_move():
    world = dc.World()

    selected = world.add_entities(
        {dc.position.x: [10, 20, 30],
         dc.position.y: [30, 40, 50],
         dc.velocity.x: 0, 
         dc.velocity.y: 0,
         dc.run_acceleration: 10,
         dc.selected: 1})

    world.add_entities(
        {dc.position.x: [10, 20, 30], dc.position.y: [30, 40, 50],
         dc.velocity.x: 0, dc.velocity.y: 0,
         dc.run_acceleration: 10})

    dc.initiate_movement(world, 400, 500)
    commanded = world[dc.move_command]
    assert set(commanded.index) == set(selected)
    assert all(commanded[dc.X] == 400)
    assert all(commanded[dc.Y] == 500)


def test_moving_units_accelerate_and_increment_by_vel():

    world = dc.World()

    moving  = world.add_entities(
        {dc.position.x: [0, 10], dc.position.y: [0, 10],
         dc.velocity.x: [0, 10], dc.velocity.y: [0, -10],
         dc.run_acceleration: np.sqrt(200),
         dc.move_command.x: [100, 100], dc.move_command.y: [100, 100]})

    dc.move(world, 1)
    # TODO: this sort of works but error is about 0.5
    assert np.allclose(
        world[dc.velocity].loc[moving].values,
        [[10, 10],
         [20, 0]], atol=0.5)
    assert np.allclose(
        world[dc.position].loc[moving].values,
        [[10, 10],
         [30, 10]], atol=0.5)


def test_moving_units_stop_when_target_is_reached():
    world = dc.World()

    moving = world.add_entities(
        {dc.position.x: [0, 80], dc.position.y: [0, 80],
         dc.velocity.x: [20, 20], dc.velocity.y: [20, 20],
         dc.run_acceleration: np.sqrt(200),
         dc.move_command.x: [101, 101], dc.move_command.y: [101, 101]})
    
    for _ in range(50):
        dc.move(world, 0.01)
    assert len(world[dc.move_command]) == 2
    for _ in range(50):
        dc.move(world, 0.01)
    assert moving[1] not in world[dc.move_command].index
    assert np.allclose(world[dc.position].loc[moving[1]].values,
                       [101, 101])


def test_select_one_idle():
    world = dc.Encounter()
    movers = world.add_entities(
        {dc.position.x: [0, 80], dc.position.y: [0, 80],
         dc.velocity.x: [20, 20], dc.velocity.y: [20, 20],
         dc.run_acceleration: np.sqrt(200)})
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
