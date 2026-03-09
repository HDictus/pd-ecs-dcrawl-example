"""Minimalistic dungeon crawler."""
import numpy as np
from pd_ecs import Component, World
import pandas as pd


move_x = Component('move to x (meters)')
move_y = Component('move to y (meters)')

position_x = Component('x (meters)')
position_y = Component('y (meters)')

velocity_x = Component('vx (m/s)')
velocity_y = Component('vy (m/s)')

max_health = Component('max health')
current_health = Component('current health')

attack_angle = Component('attack angle (radians)')
attack_dist = Component('attack dist')

run_acceleration = Component(name="run_acceleration")
selected = Component(name="selected by")
player = Component("player")
size = Component("size (radius)")
targets_closest = Component("targets player", dtype=bool)

touch_damage = Component("touch damage")

angle = Component('angle (radians)')
turn_speed = Component('turn speed')
extend_speed = Component('extend speed')

CAN_MOVE = [position_x, position_y, velocity_x, velocity_y, run_acceleration, ~move_x]


def initiate_movement(world, x, y):
    """Issue move command to selected units."""
    will_move = world[
        [
            selected,
        ]
        + CAN_MOVE
    ]

    world.give(will_move.index, {move_x: x, move_y: y})
    world.take(will_move.index, selected)


MOVING = [position_x, position_y, velocity_x, velocity_y, move_x, move_y, run_acceleration]

def _attack_if_at_end_of_movement(world, ids, unit_vectors):
    attacks = world[player].index.intersection(ids)
    if len(attacks) == 0:
        return
    direction = np.atan2(unit_vectors[:, 1], unit_vectors[:, 0])
    for entity, direc in zip(attacks, direction):
        character_attacks(world, entity, direc)

def move(world, dt):
    """Accelerate commanded units toward target location."""
    moving = world[MOVING]
    if len(moving) == 0:
        return
    idx = moving.index

    targets = moving[[move_x, move_y]].values.astype(float)
    positions = moving[[position_x, position_y]].values.astype(float)
    velocities = moving[[velocity_x, velocity_y]].values.astype(float)
    acceleration = moving[run_acceleration].values

    diffs = targets - positions
    distances = np.linalg.norm(diffs, axis=-1)[..., np.newaxis]
    unit_vectors = diffs / distances
    velocities += unit_vectors * acceleration[..., np.newaxis] * dt
    positions += velocities * dt

    passing_point = distances[..., 0] < (np.linalg.norm(velocities, axis=-1) * dt)
    positions[passing_point] = targets[passing_point]
    velocities[passing_point] = 0.0
    stopping = idx[passing_point]
    world.take(stopping, move_x, move_y)

    world.update({
        position_x: pd.Series(positions[:, 0], index=idx),
        position_y: pd.Series(positions[:, 1], index=idx),
        velocity_x: pd.Series(velocities[:, 0], index=idx),
        velocity_y: pd.Series(velocities[:, 1], index=idx),
    })
    if len(stopping):
        _attack_if_at_end_of_movement(world, stopping, unit_vectors[passing_point])


def select_idle(world):
    """Select units that are idle."""
    if len(world[selected]) > 0:
        return
    idle = world[CAN_MOVE + [player]]
    if len(idle) == 0:
        return
    world.give(idle.index.values[:1], {selected: 1})


def _sqeuclidean(x):
    return (x**2).sum(axis=-1)


# TODO: keep a kdtree for collision and nearest
def enemy_attacks(world, dt):
    idle_enemies = world[[targets_closest, ~move_x]]
    enemies = world[[position_x, position_y, touch_damage, size]]
    players = world[[position_x, position_y, player, size, current_health]]
    if len(players) == 0 or len(enemies) == 0:
        return
    squaredist = _sqeuclidean(
        enemies[[position_x, position_y]].values[:,np.newaxis] - players[[position_x, position_y]].values[np.newaxis]
    )
    in_contact = (squaredist < (
        enemies[size].values[:, np.newaxis] + players[size].values[np.newaxis]
    )**2).nonzero()

    nearest = players.index[squaredist.argmin(axis=1)]
    target_positions = players.loc[nearest]
    world.give(enemies.index, {
        move_x: target_positions[position_x].values,
        move_y: target_positions[position_y].values,
    })
    contacts = pd.DataFrame({
        'damage': enemies[touch_damage].values[in_contact[0]],
        'player': players.index.values[in_contact[1]],
    })
    damage = contacts.groupby('player')['damage'].sum() * dt
    current = world[current_health].loc[damage.index]
    world.loc[damage.index, current_health] = (current - damage.values).values


def character_attacks(world, character, direc):
    world.give(character, {attack_angle: direc, attack_dist: world.loc[character, size]})


def update_attacks(world, dt):
    attacking = world[[attack_angle, attack_dist, angle, turn_speed, extend_speed]]
    if len(attacking) == 0:
        return
    diff = np.arccos(np.cos(attacking[attack_angle] - attacking[angle]))
    turn = attacking[turn_speed] * dt
    attacking[angle] += np.sign(diff) * turn
    stopping = attacking.index[np.abs(diff) < turn]

    attacking.loc[stopping, angle] = attacking.loc[stopping, attack_angle].values
    attacking[attack_dist] += attacking[extend_speed] * dt
    world.update({
        attack_angle: attacking[attack_angle],
        attack_dist: attacking[attack_dist],
        angle: attacking[angle],
    })
    world.take(stopping, attack_angle, attack_dist)


class Encounter(World):
    """State manager for ingame encounters."""

    def time_passes(self, dt):
        """Main loop."""
        enemy_attacks(self, dt)
        update_attacks(self, dt)
        move(self, dt)
        select_idle(self)

    def add_character(self):
        """ "Add a character (for testing purposes)."""
        return self.add_entities(
            {
                position_x: 25,
                position_y: 25,
                velocity_x: 0,
                velocity_y: 0,
                run_acceleration: [900],
                max_health: 10,
                angle: 0.,
                turn_speed: np.pi * 2,
                extend_speed: 100,
                size: 10.,
                player: True,
                current_health: 10,
            }
        )

    def add_enemy(self):
        return self.add_entities(
            {
                position_x: 100,
                position_y: 100,
                velocity_x: 0,
                velocity_y: 0,
                run_acceleration: [100],
                max_health: 10,
                current_health: 10,
                targets_closest: True,
                touch_damage: 10,
                size: 20,
            }
        )

    def select_character(self, char):
        """Select a character."""
        self.give(char, {selected: 1})
