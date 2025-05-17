from game_tree import GameTree

class BattleOfTheSexes:
    def __init__(self):
        self.payoffs = {
            ('Opera', 'Opera'): (3, 2),
            ('Opera', 'Football'): (0, 0),
            ('Football', 'Opera'): (0, 0),
            ('Football', 'Football'): (2, 3)
        }
        self.players = ['Player 1', 'Player 2']
        self.strategies = ['Opera', 'Football']
    
    def find_nash_equilibrium(self):
        pure_nash = [('Opera', 'Opera'), ('Football', 'Football')]
        mixed_nash = {
            'Player 1': {'Opera': 0.4, 'Football': 0.6},
            'Player 2': {'Opera': 0.6, 'Football': 0.4}
        }
        return {'pure': pure_nash, 'mixed': mixed_nash}
    
    def calculate_expected_payoffs(self, mixed_strategy):
        p1_strat = mixed_strategy['Player 1']
        p2_strat = mixed_strategy['Player 2']
        
        p1_payoff = p2_payoff = 0
        
        for s1, prob1 in p1_strat.items():
            for s2, prob2 in p2_strat.items():
                payoff = self.payoffs[(s1, s2)]
                p1_payoff += prob1 * prob2 * payoff[0]
                p2_payoff += prob1 * prob2 * payoff[1]
        
        return (p1_payoff, p2_payoff)
    
    def display_normal_form(self):
        print("Battle of the Sexes - Normal Form")
        print("Player 2: Opera\tFootball")
        print("Player 1:")
        print(f"Opera\t\t{self.payoffs[('Opera','Opera')]}\t{self.payoffs[('Opera','Football')]}")
        print(f"Football\t{self.payoffs[('Football','Opera')]}\t{self.payoffs[('Football','Football')]}")

    def display_extensive_form(self):
        tree = GameTree()
        tree.level_height = 1.5
        
        # Root node
        tree.add_node("root", "Player 1", level=0)
        
        # Player 1 actions
        tree.add_node("P1_O", "Opera", level=1, position=(-1.5, -1))
        tree.add_node("P1_F", "Football", level=1, position=(1.5, -1))
        tree.add_edge("root", "P1_O", "Opera")
        tree.add_edge("root", "P1_F", "Football")
        
        # Player 2 actions
        for p1_action, x_pos in [("O", -1.5), ("F", 1.5)]:
            for p2_action in ["O", "F"]:
                node_id = f"P2_{p1_action}_{p2_action}"
                payoff = self._get_payoff_for_tree(p1_action, p2_action)
                tree.add_node(node_id, f"Payoff: {payoff}", level=2, 
                            position=(x_pos + (0.8 if p2_action == "F" else -0.8), -2.5))
                tree.add_edge(f"P1_{p1_action}", node_id, 
                            "Opera" if p2_action == "O" else "Football")
        
        tree.draw("Battle of the Sexes - Extensive Form")
    
    def _get_payoff_for_tree(self, p1_action, p2_action):
        p1_strat = "Opera" if p1_action == "O" else "Football"
        p2_strat = "Opera" if p2_action == "O" else "Football"
        return self.payoffs[(p1_strat, p2_strat)]