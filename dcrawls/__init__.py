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
        if character[0] in self.can_move.index:
            self.world.give(character,
                            {move_command: {X: x, Y: y}})
            return
        comps = {column[0] for column in self.can_move}
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
        diffs = self.moving[move_command] - self.moving[position]
        print(self.moving)
        print(diffs)
        directions = diffs / np.linalg.norm(diffs, axis=1)
        self.moving[velocity] += directions * self.moving[run_acceleration]
        self.moving[position] += self.moving[velocity]


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
                                  acceleration: {acceleration}})
