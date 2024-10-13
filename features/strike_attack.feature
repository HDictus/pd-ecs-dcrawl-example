Feature: player characters attack when they move

Scenario: player character strikes on move
  Given the game is in an encounter
  And the player has some characters
  And a character is walking to a point
  When the character arrives
  Then the character swings their weapon


Scenario: strike damages enemy
  Given the game is in an encounter
  And the player has some characters
  And there is an enemy
  And one of them is swinging their weapon
  When the weapon makes contact with an enemy
  Then the enemy should take damage