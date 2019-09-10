import sys

from random import random
from pmemoize import MemoizedFunction

sys.setrecursionlimit(10000)

@MemoizedFunction
def strat(d, m):
    z = 1.25 + (1 if d < 0 else 0)
    if z < 0.25:
        z = 0.25
    p = z/90.
    if p >= 1.:
        p = .99
    return p, p

@MemoizedFunction
def E(
    m, d,
    time_step,
    pts_win, pts_draw, pts_loss
):
    if m >= 90:
        if d < 0:
            return pts_loss
        elif d == 0:
            return pts_draw
        elif d > 0:
            return pts_win
    else:
        p_score, p_concede = strat(d, m)

        assert 1. > p_score > 0., p_score
        assert 1. > p_concede > 0., p_concede

        p_score *= time_step
        p_concede *= time_step

        assert 1. > p_score > 0., p_concede
        assert 1. > p_concede > 0., p_concede

        p_only_i_score = p_score * (1.-p_concede)
        p_only_opp_scores = (1.-p_score) * p_concede
        p_no_change = 1. - p_only_i_score - p_only_opp_scores

        assert 1. > p_only_i_score > 0., p_only_i_score
        assert 1. > p_only_opp_scores > 0., p_only_opp_scores
        assert 1. > p_no_change > 0., p_no_change

        return (
            p_only_i_score * E(
                m + time_step,
                d+1,
                time_step,
                pts_win, pts_draw, pts_loss
            )
                +
            p_only_opp_scores * E(
                m + time_step,
                d-1,
                time_step,
                pts_win, pts_draw, pts_loss
            )
                +
            p_no_change * E(
                m + time_step,
                d,
                time_step,
                pts_win, pts_draw, pts_loss
            )
        )

def main():
    print(E(0, 0,
        .5,
        2., 1., 0.))

main()
