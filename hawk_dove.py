from game_tree import GameTree

class HawkDoveGame:
    def __init__(self, value=4, cost=2):
        self.value = value
        self.cost = cost
        self.players = ['Player 1', 'Player 2']
        self.strategies = ['Hawk', 'Dove']
    
    def get_payoff(self, strategies):
        s1, s2 = strategies
        if s1 == 'Hawk' and s2 == 'Hawk':
            return ((self.value - self.cost)/2, (self.value - self.cost)/2)
        elif s1 == 'Hawk' and s2 == 'Dove':
            return (self.value, 0)
        elif s1 == 'Dove' and s2 == 'Hawk':
            return (0, self.value)
        else:
            return (self.value/2, self.value/2)
    
    def find_nash_equilibrium(self):
        pure_nash = [('Hawk', 'Dove'), ('Dove', 'Hawk')]
        
        p = q = min(max(self.value / self.cost, 0), 1)
        
        mixed_nash = {
            'Player 1': {'Hawk': p, 'Dove': 1-p},
            'Player 2': {'Hawk': q, 'Dove': 1-q}
        }
        
        return {'pure': pure_nash, 'mixed': mixed_nash}
    
    def display_normal_form(self):
        print("Hawk-Dove Game - Normal Form")
        print(f"Value: {self.value}, Cost: {self.cost}")
        print("Player 2: Hawk\tDove")
        print("Player 1:")
        print(f"Hawk\t\t{self.get_payoff(('Hawk','Hawk'))}\t{self.get_payoff(('Hawk','Dove'))}")
        print(f"Dove\t\t{self.get_payoff(('Dove','Hawk'))}\t{self.get_payoff(('Dove','Dove'))}")

    def display_extensive_form(self):
        tree = GameTree()
        tree.level_height = 1.2
        
        # Root node
        tree.add_node("root", "Player 1", level=0)
        
        # Player 1 actions
        tree.add_node("P1_H", "Hawk", level=1, position=(-1.2, -1))
        tree.add_node("P1_D", "Dove", level=1, position=(1.2, -1))
        tree.add_edge("root", "P1_H", "Hawk")
        tree.add_edge("root", "P1_D", "Dove")
        
        # Player 2 actions
        for p1_action, x_pos in [("H", -1.2), ("D", 1.2)]:
            for p2_action in ["H", "D"]:
                node_id = f"P2_{p1_action}_{p2_action}"
                payoff = self.get_payoff(
                    ("Hawk" if p1_action == "H" else "Dove"),
                    ("Hawk" if p2_action == "H" else "Dove")
                )
                tree.add_node(node_id, f"Payoff: {payoff}", level=2, 
                            position=(x_pos + (0.7 if p2_action == "D" else -0.7), -2.2))
                tree.add_edge(f"P1_{p1_action}", node_id, 
                            "Hawk" if p2_action == "H" else "Dove")
        
        tree.draw("Hawk-Dove Game - Extensive Form")