Feature: Enemies attack the player characters

Scenario: enemy attacks nearest character
  Given the game is in an encounter
  And the player has some characters
  And there is an enemy
  When the enemy is idle
  Then the enemy should move to the nearest player character


Scenario: touching an enemy deals damage
  Given the game is in an encounter
  And the player has some characters
  And there is an enemy
  And one of them is touching an enemy
  When time passes 
  Then the character should take damage
