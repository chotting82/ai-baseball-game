import os
import random
import time

import pytest

from main import AIBatter, calculate_strikes_balls, DIGITS


def _play_round(length, answer):
    ai = AIBatter(length)
    ai.reset()
    for attempt in range(1, 2000):
        guess = ai.guess_number()
        strikes, balls = calculate_strikes_balls(answer, guess)
        ai.record_feedback(strikes, balls)
        if strikes == length:
            return attempt
    return attempt


@pytest.mark.parametrize(
    "length, max_avg, max_attempts",
    [
        (3, 10.0, 40),
        (4, 12.0, 50),
        (5, 15.0, 60),
    ],
)
def test_ai_simulation_performance(length, max_avg, max_attempts):
    rounds = int(os.getenv("SIM_ROUNDS", "50"))
    random.seed(20240123 + length)

    start = time.perf_counter()
    attempts_list = []
    for _ in range(rounds):
        answer = random.sample(DIGITS, length)
        attempts_list.append(_play_round(length, answer))
    duration = time.perf_counter() - start

    avg_attempts = sum(attempts_list) / len(attempts_list)
    worst_attempts = max(attempts_list)
    print(
        f"length={length} rounds={rounds} "
        f"avg={avg_attempts:.2f} max={worst_attempts} "
        f"time={duration:.3f}s"
    )

    assert avg_attempts <= max_avg
    assert worst_attempts <= max_attempts
