from random import random
from pmemoize import MemoizedFunction

@MemoizedFunction
def strat(d, m):
    z = 2.5 - 2 * (d+m/50.)
    if z < 0.5:
        z = 0.5
    p = z/90.
    return p, p

@MemoizedFunction
def E(
    m, d, 
    pts_win, pts_draw, pts_loss
):
    if m == 90:
        if d < 0:
            return pts_loss
        elif d == 0:
            return pts_draw
        elif d > 0:
            return pts_win
    else:
        p_score, p_concede = strat(d, m)
        p_only_i_score = p_score * (1.-p_concede)
        p_only_opp_scores = (1.-p_score) * p_concede
        p_no_change = 1. - p_only_i_score - p_only_opp_scores
        return (
            p_only_i_score * E(
                m+1,
                d+1,
                pts_win, pts_draw, pts_loss
            )
                +
            p_only_opp_scores * E(
                m+1,
                d-1,
                pts_win, pts_draw, pts_loss
            )
                +
            p_no_change * E(
                m+1,
                d,
                pts_win, pts_draw, pts_loss
            )
        )

def main():
    print E(0, 0,
        3., 1., 0.)

main()
