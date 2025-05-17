from prisoners_dilemma import PrisonersDilemma
from battle_of_sexes import BattleOfTheSexes
from matching_pennies import MatchingPennies
from hawk_dove import HawkDoveGame

def main():
    print("Game Theory Simulator\n")
    
    games = {
        '1': ('Prisoner\'s Dilemma', PrisonersDilemma()),
        '2': ('Battle of the Sexes', BattleOfTheSexes()),
        '3': ('Matching Pennies', MatchingPennies()),
        '4': ('Hawk-Dove Game', HawkDoveGame())
    }
    
    while True:
        print("\nSelect a game to analyze:")
        for key, (name, _) in games.items():
            print(f"{key}. {name}")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '5':
            break
        elif choice in games:
            name, game = games[choice]
            print(f"\nAnalyzing {name}")
            
            print("\n=== Normal Form ===")
            game.display_normal_form()
            
            print("\n=== Extensive Form ===")
            game.display_extensive_form()
            
            if hasattr(game, 'find_nash_equilibrium'):
                print("\n=== Nash Equilibria ===")
                nash_eq = game.find_nash_equilibrium()
                print(f"Nash Equilibria: {nash_eq}")
            
            if hasattr(game, 'calculate_expected_payoffs') and isinstance(nash_eq, dict) and 'mixed' in nash_eq:
                payoffs = game.calculate_expected_payoffs(nash_eq['mixed'])
                print(f"Expected Payoffs: {payoffs}")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()