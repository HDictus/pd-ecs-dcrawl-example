from pd_ecs import World, Component
import numpy as np


X = Component('x (meters)', dtype=np.float32)
Y = Component('y (meters)', dtype=np.float32)
ACCEL = Component('accelration (m/s^2)', dtype=np.float32)


move_command = Component(x=X, y=Y, name='move_command')
position = Component(x=X, y=Y, name='position')
velocity = Component(x=X, y=Y, name='velocity')
run_acceleration = Component(name='run_acceleration')
selected = Component(name='selected by')


CAN_MOVE = [position, velocity, run_acceleration, ~move_command]


def initiate_movement(world, x, y):
    will_move = world[[selected, ] + CAN_MOVE]
    print(len(will_move))
    world.give(will_move.index, {move_command.x: x, move_command.y: y})
    world.take(will_move.index, selected)
    return


MOVING = [position, velocity, move_command, run_acceleration]


def move(world, dt):

    def _stop_at_target(posns, vels, tgts, distances):
        """
        When velocity is greater than the distance to the target, stop short
        """
        passing_point = (
            distances[..., 0] <
            np.linalg.norm(vels.values, axis=-1)*dt)
        posns[passing_point] = tgts[passing_point]
        vels[passing_point] = 0.

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
    velocities += unit_vectors * acceleration.values[..., np.newaxis] * dt
    positions += velocities * dt
    _stop_at_target(positions, velocities, targets, distances)
    world.update({position: positions, velocity: velocities})


def select_idle(world):
    if len(world[selected]) > 0:
        return
    idle = world[CAN_MOVE]
    if len(idle) == 0:
        return
    world.give(idle.index.values[:1], {selected: 1})


class Encounter(World):
    
    def time_passes(self, dt):
        move(self, dt)
        select_idle(self)

    def add_character(self):
        return self.add_entities(
            {position.x: 25, position.y: 25,
             velocity.x: 0, velocity.y: 0,
             run_acceleration: 900,
             selected: [1]})

    def select_character(self, char):
        self.loc[char, selected] = True
    
