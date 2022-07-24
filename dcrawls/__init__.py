from pd_ecs import World, Component, System
import numpy as np

X = 'x (meters)'
Y ='y (meters)'
ACCEL = 'accelration (m/s^2)'

move_command = Component(X, Y, name='move_command')
position = Component(X, Y, name='position')
velocity = Component(X, Y, name='velocity')
run_acceleration = Component(ACCEL, name='run_acceleration')


class PlayerController(System):

    def mouse_pressed(self, x, y, button=1):
        """
        command the currently selected character to go to the clicked point
        """
        self.world.events.move_command(self.selected, x, y)
        return

    def select_character(self, character_id):
        self.selected = character_id

    def mouse_released(self, x, y, button=1):
        """
        command the currently selected character to attack the clicked position
        """
        return


class Movement(System):

    filters = dict(
        can_move=[position, velocity, run_acceleration],
        moving=[position, velocity, move_command, run_acceleration])

    def move_command(self, character, x, y):
        """queue a move command for character to position x, y"""

        if character[0] in self.can_move.ids:
            self.world.give(character,
                            {move_command: {X: x, Y: y}})
            return
        comps = {column[0] for column in self.can_move.components}
        missing = []
        for comp in comps:
            if character[0] not in self.world[comp].index:
                missing.append(comp)
        raise ValueError(
            "cannot command entity to move, does not have the component(s): "
            f"{missing}")

    def update(self, dt):
        """
        Increase moving entities velocity toward their destination
        update their positions by their velocity, up to their destination
        but not further. If they have reached their destination, set their velocity to 0
        """
        posns, vels, tgts, accels = self.moving.data()
        diffs = tgts - posns
        distances = np.linalg.norm(diffs.values, axis=1)[..., np.newaxis]
        directions = diffs / distances

        vels += directions * accels.values
        posns += vels
        # __import__("pdb").set_trace()

        self._stop_at_point(posns, vels, tgts, distances)
        self.world.update({position: posns, velocity: vels})

    def _stop_at_point(self, posns, vels, tgts, distances):
        """
        When velocity is greater than the distance to the target, stop short
        """
        passing_point = distances[..., 0] < np.linalg.norm(vels.values, axis=1)
        posns[passing_point] = tgts[passing_point]
        vels[passing_point] = 0
        self.world.take(posns.index[passing_point], move_command)


class Attacking(System):

    def attack_command(self, character, x, y):
        """
        queue an attack command for character on position x, y
        """
        pass

    def update(self, dt):
        """
        progress entities attacks
        """
        pass


class Colliding(System):

    def update(self, dt):
        """
        whenever two bounding boxes overlap, register a collision event
        """
        return

    def collision(self, pairs):
        """
        process events for collided pairs of entities
        TODO: this might be a little different, working with filters
        """
        return


class Encounter(World):

    def __init__(self):
        super().__init__(position, velocity, run_acceleration, move_command)
        PlayerController(self)
        Movement(self)

    def add_character(self):
        return self.add_entities({position: {X: 123, Y: 456},
                                  velocity: {X: 0, Y: 0},
                                  run_acceleration: {ACCEL: 1}})
