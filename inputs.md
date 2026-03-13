# Bugs found:

## Sections

### Hint section:

1. Let's say the user inputs 40 as a guess and the number to be guessed is 99 then instead of saying "GO HIGHER" in HINT section,
it says "GO LOWER". Should be the other way around

### Developer Debug Info:

When the user clicks on "New Game" the following don't change back to default value

1. Score - remains same, should be set to 0
2. History - still shows the history of the previous version. Should be []

Also: 

1. The Secret or the number to be guessed some time crosses the current allowed range. For example in Easy mode it came up with 23 whereas the allowed range is 1 to 20. It should use the current range to create a new random secret value.
2. For some instances, when the game starts the "attempts" field is initialized as "1". It should be 0 at the start of the game.
3. The History is always shown till the second-last attempt. Last attempt is visible only after user makes a new attempt. History should reflect the current attempt as soon as user submits it. 

### Settings: 

1. When user switches to a different mode level (Easy, Normal, Hard) the left-handside bar correctly shows the number of attempts and the range. But the main-section still shows 1 to 100 as the range. It should be same as the current mode level

### Other bugs:

1. When user starts a new game the session memory is not updated. User can't submit a new guess. "You already won. Start a new game to play again." is shown everytime they try to submit.
2. For some instances, when the game starts the "Attempts Left" is less than the current level's total allowed attempt. It should be equal to the max total attempt allowed for the current level at the start of the game.
3. Make sure the final score is calculated properly. I believe the calculations is not correct.