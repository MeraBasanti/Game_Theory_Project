class CustomGame:
    def __init__(self, players, strategies, payoff_matrix):
        self.players = players
        self.strategies = strategies
        self.payoff_matrix = payoff_matrix
    
    def set_payoff(self, strategy_profile, payoffs):
        self.payoff_matrix[strategy_profile] = payoffs
    
    def find_nash_equilibrium(self):
        from game_analyzer import GameAnalyzer
        
        best_responses = {}
        num_players = len(self.players)
        
        for player in range(num_players):
            best_responses[player] = {}
            opponent_indices = [i for i in range(num_players) if i != player]
            
            for opp_strategies in self._get_opponent_strategies(player):
                max_payoff = -float('inf')
                best_strategy = None
                
                for strategy in self.strategies[player]:
                    strategy_profile = list(opp_strategies)
                    strategy_profile.insert(player, strategy)
                    payoff = self.payoff_matrix[tuple(strategy_profile)][player]
                    
                    if payoff > max_payoff:
                        max_payoff = payoff
                        best_strategy = strategy
                
                best_responses[player][opp_strategies] = best_strategy
        
        # Find Nash equilibria
        nash_eq = []
        for strategy_profile in self._generate_all_profiles():
            is_nash = True
            for player in range(num_players):
                opp_strategies = tuple(s for i, s in enumerate(strategy_profile) if i != player)
                if strategy_profile[player] != best_responses[player][opp_strategies]:
                    is_nash = False
                    break
            if is_nash:
                nash_eq.append(strategy_profile)
        
        return nash_eq
    
    def _get_opponent_strategies(self, player):
        from itertools import product
        other_players = [i for i in range(len(self.players)) if i != player]
        other_strategies = [self.strategies[i] for i in other_players]
        return product(*other_strategies)
    
    def _generate_all_profiles(self):
        from itertools import product
        return product(*self.strategies)