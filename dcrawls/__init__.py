from pd_ecs import World, Component
import numpy as np

X = 'x (meters)'
Y ='y (meters)'
ACCEL = 'accelration (m/s^2)'
BY='by'

move_command = Component(X, Y, name='move_command')
position = Component(X, Y, name='position')
velocity = Component(X, Y, name='velocity')
run_acceleration = Component(ACCEL, name='run_acceleration')
selected = Component('by', name='selected')


CAN_MOVE = (position, velocity, run_acceleration)


def initiate_movement(world, x, y):
    will_move = world[(selected,) + CAN_MOVE]
    world.give(will_move.index, {move_command: {X: x, Y: y}})
    return


MOVING = (position, velocity, move_command, run_acceleration)


def move(world, dt):

    def _stop_at_target(posns, vels, tgts, distances):
        """
        When velocity is greater than the distance to the target, stop short
        """
        passing_point = distances[..., 0] < np.linalg.norm(vels.values, axis=-1)
        posns[passing_point] = tgts[passing_point]
        vels[passing_point] = 0
        world.take(posns.index[passing_point], move_command)
        # TODO: we should be aware of the possibility of removing a component from an entity,
        # and then accidentally re-adding it with an .update()
        # what should the expected behavior be in this case?

    moving = world[MOVING]
    targets = moving[move_command]
    positions = moving[position].copy()
    velocities = moving[velocity].copy()
    acceleration = moving[run_acceleration]

    diffs = targets - positions
    distances = np.linalg.norm(diffs.values, axis=-1)[..., np.newaxis]
    unit_vectors = diffs / distances
    velocities += unit_vectors * acceleration.values * dt
    positions += velocities * dt
    _stop_at_target(positions, velocities, targets, distances)
    world.update({position: positions, velocity: velocities})
