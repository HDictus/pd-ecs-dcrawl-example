"""Minimalistic dungeon crawler."""
import numpy as np
from pd_ecs import Component, World
import pandas as pd


X = Component("x (meters)", dtype=np.float32)
Y = Component("y (meters)", dtype=np.float32)
ACCEL = Component("accelration (m/s^2)", dtype=np.float32)


move_command = Component(x=X, y=Y, name="move_command")
position = Component(x=X, y=Y, name="position")
velocity = Component(x=X, y=Y, name="velocity")
run_acceleration = Component(name="run_acceleration")
selected = Component(name="selected by")
player = Component("player")
size = Component("size (radius)")
targets_closest = Component("targets player", dtype=bool)
health = Component(current=Component("current"), max=Component("max"), name="health")
touch_damage = Component("touch damage")

angle = Component('angle (radians)')
dist = Component('dist')
turn_speed = Component('turn speed')
extend_speed = Component('extend speed')
attack = Component(angle=angle, dist=dist, name='attack action')

CAN_MOVE = [position, velocity, run_acceleration, ~move_command]


def initiate_movement(world, x, y):
    """Issue move command to selected units."""
    will_move = world[
        [
            selected,
        ]
        + CAN_MOVE
    ]

    world.give(will_move.index, {move_command.x: x, move_command.y: y})
    world.take(will_move.index, selected)


MOVING = [position, velocity, move_command, run_acceleration]

def _attack_if_at_end_of_movement(world, ids, unit_vectors):
    attacks = world[player].index.intersection(ids)
    if len(attacks) == 0:
        return
    direction = np.atan2(unit_vectors.values[:, 1], unit_vectors.values[:, 0])
    for entity, direc in zip(attacks, direction):
        character_attacks(world, entity, direc)

def move(world, dt):
    """Accelerate commanded units toward target location."""

    def _stop_at_target(posns, vels, tgts, distances):
        """
        When velocity is greater than the distance to the target, stop short
        """
        passing_point = distances[..., 0] < (
            np.linalg.norm(vels.values, axis=-1) * dt)
        posns[passing_point] = tgts[passing_point]
        vels[passing_point] = 0.0
        stopping = posns.index[passing_point]
        world.take(stopping, move_command)
        return stopping

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
    stopping = _stop_at_target(positions, velocities, targets, distances)
    world.update({position: positions, velocity: velocities})
    if len(stopping):
        _attack_if_at_end_of_movement(world, stopping, unit_vectors.loc[stopping])


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
    idle_enemies = world[[targets_closest, ~move_command]]
    enemies = world[[position, touch_damage, size]]
    players = world[[position, player, size, health]]
    if len(players) == 0 or len(enemies) == 0:
        return
    squaredist = _sqeuclidean(
        enemies[position].values[:,np.newaxis] - players[position].values[np.newaxis]
    )
    in_contact = (squaredist < (
        enemies[size].values[:, np.newaxis] + players[size].values[np.newaxis]
    )**2).nonzero()

    nearest = players.index[squaredist.argmin(axis=1)]
    target_positions = players.loc[nearest]
    world.give(enemies.index, {
        move_command.x: target_positions[position.x],
        move_command.y: target_positions[position.y]
    })
    contacts = pd.DataFrame({
        'damage': enemies[touch_damage].values[in_contact[0]],
        'player': players.index.values[in_contact[1]],
    })
    damage = contacts.groupby('player')['damage'].sum() * dt
    world.loc[damage.index, health.current] -= damage.values


def character_attacks(world, character, angle):
    world.give(character, {attack.angle: angle, attack.dist: world.loc[character, size]})    


def update_attacks(world, dt):
    attacking = world[[attack, angle, turn_speed, extend_speed]]
    if len(attacking) == 0:
        return
    diff = np.arccos(np.cos(attacking[attack.angle] - attacking[angle]))
    turn =  attacking[turn_speed] * dt
    attacking[angle] += np.sign(diff) * turn
    stopping = attacking.index[np.abs(diff) < turn]

    attacking.loc[stopping, angle] = attacking.loc[stopping, attack.angle].values
    attacking[attack.dist] += attacking[extend_speed] * dt
    world.loc[attacking.index, [attack, angle]] = attacking[[attack, angle]].values
    world.take(stopping, attack)


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
                position.x: 25,
                position.y: 25,
                velocity.x: 0,
                velocity.y: 0,
                run_acceleration: [900],
                health.max: 10,
                angle: 0.,
                turn_speed: np.pi * 2,
                extend_speed: 100,
                size: 10.,
                player: True,
                health.current: 10,
            }
        )

    def add_enemy(self):
        return self.add_entities(
            {
                position.x: 100,
                position.y: 100,
                velocity.x: 0,
                velocity.y: 0,
                run_acceleration: [100],
                health.max: 10,
                health.current: 10,
                targets_closest: True,
                touch_damage: 10,
                size: 20,
            }
        )

    def select_character(self, char):
        """Select a character."""
        self.give(char, {selected: 1})
