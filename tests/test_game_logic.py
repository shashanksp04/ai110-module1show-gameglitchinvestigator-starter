from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# --- Original tests (fixed: check_guess returns (outcome, message)) ---


def test_winning_guess():
    """If the secret is 50 and guess is 50, it should be a win."""
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    """If secret is 50 and guess is 60, hint should be "Too High"."""
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    """If secret is 50 and guess is 40, hint should be "Too Low"."""
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug: Hint logic inverted (too low said "Go LOWER!", too high said "Go HIGHER!") ---


def test_hint_too_high_returns_go_lower():
    """When guess is too high, message must say Go LOWER! (not Go HIGHER!)."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_hint_too_low_returns_go_higher():
    """When guess is too low, message must say Go HIGHER! (not Go LOWER!)."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


# --- Bug: TypeError path / string comparison (e.g. "100" < "98") ---


def test_check_guess_int_and_str_same_value_returns_win():
    """When guess and secret are same number but one is str, must still return Win."""
    outcome, _ = check_guess(50, "50")
    assert outcome == "Win"
    outcome, _ = check_guess("50", 50)
    assert outcome == "Win"


def test_check_guess_int_str_numeric_comparison_low():
    """Guess 40 vs secret '99' must be Too Low with Go HIGHER (not string compare)."""
    outcome, message = check_guess(40, "99")
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_check_guess_int_str_numeric_comparison_high():
    """Guess 99 vs secret '40' must be Too High with Go LOWER."""
    outcome, message = check_guess(99, "40")
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


# --- Bug: Secret outside current difficulty range (e.g. 23 in Easy 1–20) ---


def test_get_range_easy_is_1_to_20():
    """Easy mode must use range 1–20 so secret is always in [1, 20]."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20


def test_get_range_normal_is_1_to_100():
    """Normal mode must use range 1–100."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100


def test_get_range_hard_is_1_to_50():
    """Hard mode must use range 1–50."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 50


def test_get_range_bounds_allow_valid_secret():
    """Returned low <= high so random.randint(low, high) is valid."""
    for difficulty in ("Easy", "Normal", "Hard"):
        low, high = get_range_for_difficulty(difficulty)
        assert low <= high


# --- Bug: Attempts started at 1 / Attempts Left less than max at start ---
# (Logic layer: no direct "attempts" state; app uses 0 now. Test that attempt_number
# in update_score is used correctly so attempt 1 = first attempt.)


def test_update_score_win_attempt_1_gives_90_points():
    """Win on first attempt (attempt_number=1) must add 90, not 80 (formula was +1 off)."""
    new_score = update_score(0, "Win", 1)
    assert new_score == 90


# --- Bug: Final score formula (attempt_number+1 made win points one step too low) ---


def test_update_score_win_attempt_2_gives_80_points():
    """Win on second attempt must add 80 points."""
    new_score = update_score(0, "Win", 2)
    assert new_score == 80


def test_update_score_win_minimum_10_points():
    """Win on many attempts must still add at least 10 points."""
    new_score = update_score(0, "Win", 15)
    assert new_score >= 10


def test_update_score_win_cumulative():
    """Score accumulates: win on attempt 1 from 0 gives 90."""
    new_score = update_score(100, "Win", 1)
    assert new_score == 190


# --- Bug: New Game reset (score 0, history [], status) and Settings range ---
# (Those are app/session behaviors; get_range_for_difficulty already tested above
# so main section can use low/high. parse_guess is used for input validation.)


def test_parse_guess_empty_returns_error():
    """Empty or missing input must return ok=False and ask for a guess."""
    ok, _, err = parse_guess("")
    assert ok is False
    assert err is not None


def test_parse_guess_non_number_returns_error():
    """Non-numeric input must return ok=False."""
    ok, _, err = parse_guess("abc")
    assert ok is False
    assert "number" in err.lower() or err


def test_parse_guess_valid_integer_returns_ok():
    """Valid integer string must parse and return ok=True."""
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None
