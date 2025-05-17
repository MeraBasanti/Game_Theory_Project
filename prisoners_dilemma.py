from game_tree import GameTree
from game_analyzer import GameAnalyzer

class PrisonersDilemma:
    def __init__(self):
        self.payoffs = {
            ('Cooperate', 'Cooperate'): (-1, -1),
            ('Cooperate', 'Defect'): (-3, 0),
            ('Defect', 'Cooperate'): (0, -3),
            ('Defect', 'Defect'): (-2, -2)
        }
        self.players = ['Player 1', 'Player 2']
        self.strategies = ['Cooperate', 'Defect']

    def analyze_strategies(self):
        analyzer = GameAnalyzer()
        
        print("\n=== Pure Strategy Analysis ===")
        pure_eq = analyzer.find_pure_strategy_equilibria(self.payoffs)
        print(f"Pure Strategy Nash Equilibria: {pure_eq}")
        
        print("\n=== Mixed Strategy Analysis ===")
        mixed_eq = analyzer.find_mixed_strategy_equilibrium(
            self.payoffs, self.strategies, self.strategies)
        print(f"Mixed Strategy Nash Equilibrium: {mixed_eq}")
        
        if mixed_eq:
            expected_payoffs = analyzer.calculate_expected_payoffs(
                self.payoffs, 
                {0: mixed_eq['Player 1'], 1: mixed_eq['Player 2']}
            )
            print(f"Expected Payoffs in Mixed NE: {expected_payoffs}")
        
        print("\n=== Dominance Analysis ===")
        for player, strategy in enumerate(self.strategies):
            dominated = analyzer.is_strategy_dominated(self.payoffs, player, strategy)
            print(f"{self.players[player]}'s strategy '{strategy}' is dominated: {dominated}")
        
        print("\n=== Best Response Analysis ===")
        for player in [0, 1]:
            print(f"\n{self.players[player]}'s best responses:")
            opponent = 1 - player
            for opp_strategy in self.strategies:
                br = analyzer.find_best_response(self.payoffs, player, [opp_strategy])
                print(f"Against {opp_strategy}: {br}")
    
    def get_payoff(self, strategies):
        return self.payoffs[strategies]
    
    def find_nash_equilibrium(self):
        best_responses = {0: {}, 1: {}}
        
        for player in [0, 1]:
            opponent = 1 - player
            for opp_strategy in self.strategies:
                max_payoff = -float('inf')
                best_strategy = None
                for strategy in self.strategies:
                    if player == 0:
                        payoff = self.payoffs[(strategy, opp_strategy)][player]
                    else:
                        payoff = self.payoffs[(opp_strategy, strategy)][player]
                    if payoff > max_payoff:
                        max_payoff = payoff
                        best_strategy = strategy
                best_responses[player][opp_strategy] = best_strategy
        
        nash_eq = []
        for s1 in self.strategies:
            for s2 in self.strategies:
                if (best_responses[0][s2] == s1 and 
                    best_responses[1][s1] == s2):
                    nash_eq.append((s1, s2))
        
        return nash_eq
    
    def display_normal_form(self):
        print("Prisoner's Dilemma - Normal Form")
        print("Player 2: Cooperate\tDefect")
        print("Player 1:")
        print(f"Cooperate\t{self.payoffs[('Cooperate','Cooperate')]}\t{self.payoffs[('Cooperate','Defect')]}")
        print(f"Defect\t\t{self.payoffs[('Defect','Cooperate')]}\t{self.payoffs[('Defect','Defect')]}")

    def display_extensive_form(self):
        tree = GameTree()
        
        # Root node
        tree.add_node("root", "Nature", level=0)
        
        # Player 1 decision
        tree.add_node("P1", "Player 1", level=1, position=(-1.5, 0))
        tree.add_node("P1_2", "Player 1", level=1, position=(1.5, 0))
        tree.add_edge("root", "P1", "50%")
        tree.add_edge("root", "P1_2", "50%")
        
        # Player 1 actions
        tree.add_node("P1_C", "Cooperate", level=2, position=(-2, -1))
        tree.add_node("P1_D", "Defect", level=2, position=(-1, -1))
        tree.add_edge("P1", "P1_C", "Cooperate")
        tree.add_edge("P1", "P1_D", "Defect")
        
        tree.add_node("P1_C2", "Cooperate", level=2, position=(1, -1))
        tree.add_node("P1_D2", "Defect", level=2, position=(2, -1))
        tree.add_edge("P1_2", "P1_C2", "Cooperate")
        tree.add_edge("P1_2", "P1_D2", "Defect")
        
        # Player 2 actions
        for p1_action, x_pos in [("C", -2), ("D", -1), ("C2", 1), ("D2", 2)]:
            for p2_action in ["C", "D"]:
                node_id = f"P2_{p1_action}_{p2_action}"
                payoff = self._get_payoff_for_tree(p1_action, p2_action)
                tree.add_node(node_id, f"Payoff: {payoff}", level=3, 
                            position=(x_pos + (0.5 if p2_action == "D" else -0.5), -2))
                tree.add_edge(f"P1_{p1_action}", node_id, 
                            "Cooperate" if p2_action == "C" else "Defect")
        
        tree.draw("Prisoner's Dilemma - Extensive Form")
    
    def _get_payoff_for_tree(self, p1_action, p2_action):
        # Map tree actions to actual strategies
        p1_strat = "Cooperate" if "C" in p1_action else "Defect"
        p2_strat = "Cooperate" if p2_action == "C" else "Defect"
        return self.payoffs[(p1_strat, p2_strat)]