from game_tree import GameTree

class MatchingPennies:
    def __init__(self):
        self.payoffs = {
            ('Heads', 'Heads'): (1, -1),
            ('Heads', 'Tails'): (-1, 1),
            ('Tails', 'Heads'): (-1, 1),
            ('Tails', 'Tails'): (1, -1)
        }
        self.players = ['Player 1', 'Player 2']
        self.strategies = ['Heads', 'Tails']
    
    def find_nash_equilibrium(self):
        return {
            'Player 1': {'Heads': 0.5, 'Tails': 0.5},
            'Player 2': {'Heads': 0.5, 'Tails': 0.5}
        }
    
    def is_zero_sum(self):
        return True
    
    def display_normal_form(self):
        print("Matching Pennies - Normal Form")
        print("Player 2: Heads\tTails")
        print("Player 1:")
        print(f"Heads\t\t{self.payoffs[('Heads','Heads')]}\t{self.payoffs[('Heads','Tails')]}")
        print(f"Tails\t\t{self.payoffs[('Tails','Heads')]}\t{self.payoffs[('Tails','Tails')]}")

    def display_extensive_form(self):
        tree = GameTree()
        tree.node_width = 1.5
        
        # Root node
        tree.add_node("root", "Player 1", level=0)
        
        # Player 1 actions
        tree.add_node("P1_H", "Heads", level=1, position=(-1, -1))
        tree.add_node("P1_T", "Tails", level=1, position=(1, -1))
        tree.add_edge("root", "P1_H", "Heads")
        tree.add_edge("root", "P1_T", "Tails")
        
        # Player 2 actions
        for p1_action, x_pos in [("H", -1), ("T", 1)]:
            for p2_action in ["H", "T"]:
                node_id = f"P2_{p1_action}_{p2_action}"
                payoff = self._get_payoff_for_tree(p1_action, p2_action)
                tree.add_node(node_id, f"Payoff: {payoff}", level=2, 
                            position=(x_pos + (0.5 if p2_action == "T" else -0.5), -2))
                tree.add_edge(f"P1_{p1_action}", node_id, 
                            "Heads" if p2_action == "H" else "Tails")
        
        tree.draw("Matching Pennies - Extensive Form")
    
    def _get_payoff_for_tree(self, p1_action, p2_action):
        p1_strat = "Heads" if p1_action == "H" else "Tails"
        p2_strat = "Heads" if p2_action == "H" else "Tails"
        return self.payoffs[(p1_strat, p2_strat)]