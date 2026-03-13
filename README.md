# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
  - It is a number-guessing game where the player tries to find a secret number within the given range. The player chooses a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), gets a limited number of attempts, and receives "Go higher" or "Go lower" hints after each guess. Scoring rewards winning in fewer attempts and penalizes wrong guesses. The goal is to guess the secret number before running out of attempts and to earn the highest score.
- [X] Detail which bugs you found.
  - The hint logic was inverted: when the guess was too low it said "Go LOWER!" and when too high it said "Go HIGHER!". On even attempts the app passed the secret as a string, so comparisons used the TypeError path and string comparison (e.g. "100" < "98"), producing wrong outcomes.
  - **Developer Debug Info:** New Game did not reset Score (stayed same) or History (still showed previous). Secret could be outside current difficulty range (e.g. 23 in Easy 1–20). Attempts sometimes started at 1 instead of 0. History showed only up to second-last attempt until next submit.
  - **Settings:** Main section always showed "1 to 100" instead of the current mode’s range.
  - **Other:** New Game did not reset session status, so after winning the user could not submit again. Attempts Left could be less than the level max at start. Final score formula used `attempt_number + 1`, making win points one step too low.
  - **Hint section:** Hints stopped showing in the hint area even when "Show hint" was checked. This worked originally; it broke after adding `st.rerun()` to fix the Developer Debug History bug—the hint was rendered inside the submit block, then the rerun cleared the page so the hint never stayed visible.
  - **Win message and balloons:** After guessing correctly, the user saw "You already won. Start a new game to play again." instead of balloons and the win message (secret + final score). Same cause: the win UI was rendered in the submit block, then `st.rerun()` ran and on the next run only the generic "already won" message was shown.
- [X] Explain what fixes you applied.
  - Refactored backend logic out of app.py into logic_utils.py (get_range_for_difficulty, parse_guess, check_guess, update_score).
  - app.py now imports these functions from logic_utils; the UI code is unchanged.
  - Fixed the hint messages in logic_utils.py so "Too High" returns "Go LOWER!" and "Too Low" returns "Go HIGHER!". In the TypeError branch (when guess/secret types differ), the code now converts both to int for numeric comparison so hints are correct regardless of type.
  - **Developer Debug Info:** New Game now sets score = 0, history = [], and status = "playing". New secret uses current (low, high) from difficulty; secret is regenerated when outside current range. Initial attempts set to 0. After each submit, call st.rerun() so History shows the current attempt immediately.
  - **Settings:** Main-section message now uses `low` and `high` from get_range_for_difficulty instead of hardcoded 1–100.
  - **Other:** New Game resets status to "playing" so user can submit again. Win score in logic_utils.py changed from 100 - 10*(attempt_number+1) to 100 - 10*attempt_number (min 10).
  - **Hint section:** Persist the last hint in `st.session_state.last_hint` when the user submits (and only when "Show hint" is checked), then render a dedicated "Hint" section on every run that displays `last_hint` if set. New Game clears `last_hint`. Hints now stay visible after the rerun that was added for the History fix.
  - **Win message and balloons:** When `status == "won"`, the non-playing block now shows balloons, the success message with secret and final score (from session state), and "Start a new game to play again." so the win experience is visible after the rerun.

## 📸 Demo

- [x] [Insert a screenshot of your fixed, winning game here]
  - kindly check demo.png

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
