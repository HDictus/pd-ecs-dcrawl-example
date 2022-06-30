Feature: giving characters move commands

Scenario: idle character is selected and time stopped
  Given the game is in an encounter
  And there are characters doing something
  When one of these characaters becomes idle
  Then time should stop
  And the idle character should be selected


Scenario: giving a move command
  Given the game is in an encounter
  And a character is selected
  When The mouse is clicked at a position
  Then the character should run there with increasing speed
  And the character should stop at that position

