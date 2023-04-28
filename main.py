"""
Implements simulation of the Coin Example from https://en.wikipedia.org/wiki/Parrondo%27s_paradox
"""

from typing import Iterable
import random
import itertools


def cointoss(p_win: float) -> int:
    r = random.random()
    return 1 if r < p_win else -1


class GameA:

    def __init__(self, p_win):
        self.p_win = p_win

    def play(self, capital: int) -> int:
        return cointoss(self.p_win)

    def __repr__(self):
        return "A"


class GameB:

    def __init__(self, p_win1: float, p_win2: float, m: int):
        self.p_win1 = p_win1
        self.p_win2 = p_win2
        self.m = m

    def play(self, capital: int) -> int:
        if capital % self.m == 0:
            return cointoss(self.p_win1)
        return cointoss(self.p_win2)

    def __repr__(self):
        return "B"


def simulate(game_seq_pattern: Iterable, n_steps: int, init_capital: int = 0):
    cnt = 0
    cap = init_capital
    for game in itertools.cycle(game_seq_pattern):
        if cnt == n_steps:
            break
        win = game.play(capital=cap)
        cap += int(win)
        cnt += 1
    return cap


if __name__ == "__main__":
    # optionally set the random seed or not
    random.seed(42)

    eps = 0.005
    M_candidates = 3, 2
    sim_steps = 10 ** 6

    for M in M_candidates:
        print(f"Running for {eps=} {M=} {sim_steps=}")

        gameA = GameA(p_win=0.5 - eps)
        gameB = GameB(p_win1=0.1 - eps, p_win2=0.75 - eps, m=M)

        resA = simulate([gameA], n_steps=sim_steps)
        if resA >= 0:
            print("WARNING: game A is not losing")
            continue

        resB = simulate([gameB], n_steps=sim_steps)
        if resB >= 0:
            print("WARNING: game B is not losing")
            continue

        AB = [gameA, gameB]
        AABB = [gameA, gameA, gameB, gameB]
        AAABBB = [gameA, gameA, gameA, gameB, gameB, gameB]
        AAB = [gameA, gameA, gameB]
        for seq in [AB, AABB, AAABBB, AAB]:
            res = simulate(game_seq_pattern=seq, n_steps=sim_steps, init_capital=0)
            if res > 0:
                print(f"\t{seq=} is winning {res=}")
            else:
                print(f"\t{seq=} is losing {res=}")









