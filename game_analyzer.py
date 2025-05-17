import numpy as np
from itertools import product

class GameAnalyzer:
    @staticmethod
    def find_pure_strategy_equilibria(payoff_matrix):
        """Find all pure strategy Nash equilibria"""
        players = range(len(next(iter(payoff_matrix.values()))))
        strategies = {
            player: list({s[player] for s in payoff_matrix.keys()})
            for player in players
        }
        
        equilibria = []
        
        for strategy_profile in payoff_matrix.keys():
            is_equilibrium = True
            for player in players:
                current_payoff = payoff_matrix[strategy_profile][player]
                
                # Check all possible deviations for this player
                for alt_strategy in strategies[player]:
                    if alt_strategy == strategy_profile[player]:
                        continue
                    
                    # Create alternative strategy profile
                    alt_profile = list(strategy_profile)
                    alt_profile[player] = alt_strategy
                    alt_profile = tuple(alt_profile)
                    
                    if payoff_matrix[alt_profile][player] > current_payoff:
                        is_equilibrium = False
                        break
                
                if not is_equilibrium:
                    break
            
            if is_equilibrium:
                equilibria.append(strategy_profile)
        
        return equilibria

    @staticmethod
    def find_mixed_strategy_equilibrium(payoff_matrix, player1_strategies, player2_strategies):
        """Calculate mixed strategy Nash equilibrium for 2-player games"""
        # Convert payoff matrix to numpy arrays for easier calculation
        p1_payoffs = np.zeros((len(player1_strategies), len(player2_strategies)))
        p2_payoffs = np.zeros((len(player1_strategies), len(player2_strategies)))
        
        # Fill payoff matrices
        for i, s1 in enumerate(player1_strategies):
            for j, s2 in enumerate(player2_strategies):
                p1_payoffs[i,j], p2_payoffs[i,j] = payoff_matrix[(s1, s2)]
        
        # Solve for Player 2's probabilities that make Player 1 indifferent
        if len(player1_strategies) == 2 and len(player2_strategies) == 2:
            # For 2x2 games, we can solve directly
            a, b = p1_payoffs[0,0] - p1_payoffs[1,0], p1_payoffs[0,1] - p1_payoffs[1,1]
            if (a - b) != 0:
                q = a / (a - b)  # Probability Player 2 plays first strategy
            else:
                q = 0.5  # If no unique solution, return 50-50
            
            c, d = p2_payoffs[0,0] - p2_payoffs[0,1], p2_payoffs[1,0] - p2_payoffs[1,1]
            if (c - d) != 0:
                p = d / (d - c)  # Probability Player 1 plays first strategy
            else:
                p = 0.5
            
            return {
                'Player 1': {player1_strategies[0]: p, player1_strategies[1]: 1-p},
                'Player 2': {player2_strategies[0]: q, player2_strategies[1]: 1-q}
            }
        else:
            # For larger games, use linear programming approach
            return GameAnalyzer.solve_mixed_equilibrium_lp(p1_payoffs, p2_payoffs, 
                                                         player1_strategies, player2_strategies)

    @staticmethod
    def solve_mixed_equilibrium_lp(p1_payoffs, p2_payoffs, p1_strats, p2_strats):
        """Solve for mixed equilibrium using linear programming"""
        from scipy.optimize import linprog
        
        # Player 1's problem: find probabilities p that make Player 2 indifferent
        num_p1 = len(p1_strats)
        num_p2 = len(p2_strats)
        
        # Objective: maximize (v) which is the minimum expected payoff
        c = np.zeros(num_p1 + 1)
        c[-1] = -1  # We're maximizing v, which is equivalent to minimizing -v
        
        # Constraints: for each of Player 2's pure strategies, Player 1's expected payoff ≥ v
        A_ub = []
        for j in range(num_p2):
            row = np.zeros(num_p1 + 1)
            row[:num_p1] = -p2_payoffs[:, j]  # Note we use p2_payoffs because we're solving for p1
            row[-1] = 1
            A_ub.append(row)
        A_ub = np.array(A_ub)
        b_ub = np.zeros(num_p2)
        
        # Probabilities sum to 1 and are non-negative
        A_eq = np.zeros((1, num_p1 + 1))
        A_eq[0, :num_p1] = 1
        b_eq = np.array([1])
        
        bounds = [(0, None) for _ in range(num_p1)] + [(None, None)]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        
        if res.success:
            p1_probs = res.x[:num_p1]
        else:
            p1_probs = np.ones(num_p1) / num_p1  # Fallback to uniform if no solution
            
        # Similarly solve for Player 2's probabilities
        c = np.zeros(num_p2 + 1)
        c[-1] = -1
        
        A_ub = []
        for i in range(num_p1):
            row = np.zeros(num_p2 + 1)
            row[:num_p2] = -p1_payoffs[i, :]
            row[-1] = 1
            A_ub.append(row)
        A_ub = np.array(A_ub)
        b_ub = np.zeros(num_p1)
        
        A_eq = np.zeros((1, num_p2 + 1))
        A_eq[0, :num_p2] = 1
        b_eq = np.array([1])
        
        bounds = [(0, None) for _ in range(num_p2)] + [(None, None)]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        
        if res.success:
            p2_probs = res.x[:num_p2]
        else:
            p2_probs = np.ones(num_p2) / num_p2
            
        return {
            'Player 1': {s: p for s, p in zip(p1_strats, p1_probs)},
            'Player 2': {s: p for s, p in zip(p2_strats, p2_probs)}
        }

    @staticmethod
    def calculate_expected_payoffs(payoff_matrix, mixed_strategy):
        """Calculate expected payoffs for a given mixed strategy profile"""
        players = range(len(next(iter(payoff_matrix.values()))))
        expected_payoffs = [0.0 for _ in players]
        
        # Get all possible pure strategy combinations
        all_strategies = [list(strats.keys()) for strats in mixed_strategy.values()]
        all_profiles = product(*all_strategies)
        
        for profile in all_profiles:
            # Calculate probability of this profile occurring
            prob = 1.0
            for player, strategy in enumerate(profile):
                prob *= mixed_strategy[player][strategy]
            
            # Add to expected payoffs
            payoffs = payoff_matrix[profile]
            for player in players:
                expected_payoffs[player] += prob * payoffs[player]
        
        return expected_payoffs

    @staticmethod
    def find_best_response(payoff_matrix, player, opponent_strategy):
        """Find best response for a player given opponent's strategy"""
        max_payoff = -float('inf')
        best_strategy = None
        strategies = list({s[player] for s in payoff_matrix.keys()})
        
        for strategy in strategies:
            # Create strategy profile with this strategy
            profile = list(opponent_strategy)
            profile.insert(player, strategy)
            payoff = payoff_matrix[tuple(profile)][player]
            
            if payoff > max_payoff:
                max_payoff = payoff
                best_strategy = strategy
        
        return best_strategy

    @staticmethod
    def is_strategy_dominated(payoff_matrix, player, strategy):
        """Check if a strategy is strictly dominated for a player"""
        other_strategies = [s for s in {s[player] for s in payoff_matrix.keys()} if s != strategy]
        
        for alt_strategy in other_strategies:
            dominated = True
            for opp_strategy in {s for p, s in enumerate(next(iter(payoff_matrix.keys()))) if p != player}:
                # Create both strategy profiles
                profile_with_strat = list(opp_strategy)
                profile_with_strat.insert(player, strategy)
                
                profile_with_alt = list(opp_strategy)
                profile_with_alt.insert(player, alt_strategy)
                
                if payoff_matrix[tuple(profile_with_strat)][player] >= payoff_matrix[tuple(profile_with_alt)][player]:
                    dominated = False
                    break
            
            if dominated:
                return True
        
        return False