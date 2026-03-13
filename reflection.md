# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - It kind of felt like it was working on the first submission. But after that things got clear on how the backend logic had bugs.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
   - **Developer Debug Info:** New Game did not reset Score (stayed same) or History (still showed previous). Secret could be outside current difficulty range (e.g. 23 in Easy 1–20). Attempts sometimes started at 1 instead of 0. History showed only up to second-last attempt until next submit.
  - **Settings:** Main section always showed "1 to 100" instead of the current mode’s range.
  - **Other:** New Game did not reset session status, so after winning the user could not submit again. Attempts Left could be less than the level max at start. Final score formula used `attempt_number + 1`, making win points one step too low.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Cursor
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - The type-check for the correct Hint message. As originally I only checked for the comparison check but Cursor pointed out the
  type check
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When working on the session updates, it made changes to that part of the code. I was skeptical about that and it did lead to two new bugs which I documented. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - ran tests and also re-ran the game to verify it
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - checking the hint suggestions, secret value updation
- Did AI help you design or understand any tests? How?
  - it helped in designing. I had priovided it inputs.md which was a list of bugs I had found.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - The script runs from top to bottom every time you click something. So the secret was being set with random again on each run instead of staying the same.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Every time you interact with the app, Streamlit runs the whole script again (that’s a rerun). Session state is where you store values that should stick around between those reruns instead of being reset.
- What change did you make that finally gave the game a stable secret number?
  - We put the secret in st.session_state and only set it when it’s not already there (or when you start a new game), so it doesn’t get reset on every rerun.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Creating inputs.md really helped!
- What is one thing you would do differently next time you work with AI on a coding task?
  - making the inputs.md more descriptive
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - I didn't feel like it was indifferent. We collaborated together so I understood every part of the code.
