from pd_ecs import World, Component, System

X = 'x (meters)'
Y ='y (meters)'

move_command = Component(X, Y)
position = Component(X, Y)


class PlayerController:

    def mouse_pressed(self, x, y, button):
        """
        command the currently selected character to go to the clicked point
        """
        self.world.events.move_command(self.selected, x, y)
        return


    def mouse_released(self, x, y, position):
        """
        command the currently selected character to attack the clicked position
        """
        return


class MovementSystem:

    def move_command(self, character, x, y):
        """queue a move command for character to position x, y"""
        self.world.give(character,
                        {move_command: {X: x, Y: y}})
        return

    def update(self, dt):
        """
        Increase moving entities velocity toward their destination
        update their positions by their velocity, up to their destination
        but not further. If they have reached their destination, set their velocity to 0
        """
        return


class AttackSystem:

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


class CollisionSystem:

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
        super().__init__(position, move_command)
        CommandSystem(self)
        MovementSystem(self)

    def add_character(self):
        return self.add_entities({position: {X: 123, Y: 456}})
