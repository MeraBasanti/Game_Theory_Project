# analysis.py
from fractions import Fraction

def calculate_game_analysis():
    """Performs game-theoretic analysis and returns content for outputs."""
    payoffs = {
        ('Ballet', 'Ballet'): (1, 2),
        ('Ballet', 'Fight'): (0, 0),
        ('Fight', 'Ballet'): (0, 0),
        ('Fight', 'Fight'): (2, 1)
    }
    
    # 1. Dominated Strategies
    dominated = []
    man_ballet = [payoffs[('Ballet', w)][0] for w in ['Ballet', 'Fight']]
    man_fight = [payoffs[('Fight', w)][0] for w in ['Ballet', 'Fight']]
    woman_ballet = [payoffs[(m, 'Ballet')][1] for m in ['Ballet', 'Fight']]
    woman_fight = [payoffs[(m, 'Fight')][1] for m in ['Ballet', 'Fight']]
    dominated_man = "Neither strategy is dominated for Man."
    dominated_woman = "Neither strategy is dominated for Woman."
    dominated_result = "No strictly dominated strategies exist."
    dominated.extend([dominated_man, dominated_woman, dominated_result])

    # 2. Best Responses
    best_responses = []
    br_man_ballet = "If Woman plays Ballet, Man's payoffs are Ballet: 1, Fight: 0. Best response: Ballet."
    br_man_fight = "If Woman plays Fight, Man's payoffs are Ballet: 0, Fight: 2. Best response: Fight."
    br_woman_ballet = "If Man plays Ballet, Woman's payoffs are Ballet: 2, Fight: 0. Best response: Ballet."
    br_woman_fight = "If Man plays Fight, Woman's payoffs are Ballet: 0, Fight: 1. Best response: Fight."
    best_responses.extend([br_man_ballet, br_man_fight, br_woman_ballet, br_woman_fight])

    # 3. Rationalizable Strategies (Corrected)
    rationalizable = (
        "We check for rationalizable strategies by performing iterated elimination of strictly dominated strategies "
        "and confirming best responses to beliefs. "
        "For Man, Ballet (payoffs: 1 if Woman plays Ballet, 0 if Fight) is not dominated by Fight (payoffs: 0 if Ballet, 2 if Fight), "
        "as 1 > 0 but 0 < 2. Similarly, for Woman, Ballet (payoffs: 2 if Man plays Ballet, 0 if Fight) is not dominated by Fight "
        "(payoffs: 0 if Ballet, 1 if Fight), as 2 > 0 but 0 < 1. Since no strategies are strictly dominated, no strategies are eliminated. "
        "Further, Ballet and Fight are best responses for Man if he believes Woman plays Ballet with probability "
        "$q \\geq \\frac{2}{3}$ or $q \\leq \\frac{2}{3}$, respectively, and for Woman if she believes Man plays Ballet with "
        "$p \\geq \\frac{1}{3}$ or $p \\leq \\frac{1}{3}$, respectively. Thus, all strategies are rationalizable. "
        "Result: Man's strategies: {Ballet, Fight}, Woman's strategies: {Ballet, Fight}."
    )

    # 4. Expected Payoffs
    expected_payoffs_man = r"E_M = q + 2(1-p)(1-q)"
    expected_payoffs_woman = r"E_W = 2p + (1-p)(1-q)"
    expected_payoffs = [expected_payoffs_man, expected_payoffs_woman]

    # 5. Pure Strategy Nash Equilibria
    pure_ne = []
    bb_check = ("(Ballet, Ballet): Man gets 1 (vs. 0 if Fight), "
                "Woman gets 2 (vs. 0 if Fight). Stable.")
    bf_check = ("(Ballet, Fight): Man gets 0 (prefers Fight for 2), "
                "Woman gets 0 (prefers Ballet for 1). Unstable.")
    fb_check = ("(Fight, Ballet): Man gets 0 (prefers Ballet for 1), "
                "Woman gets 0 (prefers Fight for 2). Unstable.")
    ff_check = ("(Fight, Fight): Man gets 2 (vs. 0 if Ballet), "
                "Woman gets 1 (vs. 0 if Ballet). Stable.")
    pure_ne_result = "Pure NE: (Ballet, Ballet) and (Fight, Fight)."
    pure_ne.extend([bb_check, bf_check, fb_check, ff_check, pure_ne_result])

    # 6. Mixed Strategy Nash Equilibrium
    q = Fraction(2, 3)
    q_steps = [
        r"q \cdot 1 + (1-q) \cdot 0 = q \cdot 0 + (1-q) \cdot 2",
        r"q = 2(1-q)",
        r"q = 2 - 2q",
        r"3q = 2",
        r"q = \frac{2}{3}"
    ]
    p = Fraction(1, 3)
    p_steps = [
        r"2p \cdot 1 + (1-p) \cdot 0 = p \cdot 0 + (1-p) \cdot 1",
        r"2p = 1-p",
        r"3p = 1",
        r"p = \frac{1}{3}"
    ]
    e_m = q
    e_w = 2 * p
    mixed_ne_result = (f"Mixed NE: Man plays Ballet with $p = {p}$, Fight with ${1-p}$; "
                       f"Woman plays Ballet with $q = {q}$, Fight with ${1-q}$. "
                       f"Expected payoffs: $E_M = {e_m}$, $E_W = {e_w}$.")

    return {
        'dominated': dominated,
        'best_responses': best_responses,
        'rationalizable': rationalizable,
        'expected_payoffs': expected_payoffs,
        'pure_ne': pure_ne,
        'mixed_ne': {
            'man_steps': p_steps,
            'woman_steps': q_steps,
            'result': mixed_ne_result
        }
    }