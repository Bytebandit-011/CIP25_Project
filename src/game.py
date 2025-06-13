from utils import load_data, save_data
import random

class Akinator:
    def __init__(self):
        # Load character database
        self.characters = load_data()
        self.current_possibilities = self.characters.copy()
        self.questions_asked = []
    
    def filter_characters(self, attribute, value):
        """Filter possible characters based on answer"""
        self.current_possibilities = [
            char for char in self.current_possibilities 
            if char.get(attribute, "").lower() == value.lower()
        ]
    
    def get_best_question(self):
        """Find the question that best splits the remaining possibilities"""
        if len(self.current_possibilities) <= 1:
            return None
            
        # Attributes to ask about (excluding name)
        possible_attributes = set()
        for char in self.current_possibilities:
            possible_attributes.update(char.keys())
        possible_attributes.discard('name')
        
        # Remove already asked questions
        available_attributes = possible_attributes - set(self.questions_asked)
        
        if not available_attributes:
            return None
        
        # Find attribute that best splits the data
        best_attribute = None
        best_split_score = float('inf')
        
        for attr in available_attributes:
            # Count how many characters have each value for this attribute
            value_counts = {}
            for char in self.current_possibilities:
                value = char.get(attr, "unknown").lower()
                value_counts[value] = value_counts.get(value, 0) + 1
            
            # Calculate how well this splits the data (closer to 50/50 is better)
            if len(value_counts) >= 2:
                values = list(value_counts.values())
                split_score = abs(values[0] - values[1]) if len(values) == 2 else min(values)
                if split_score < best_split_score:
                    best_split_score = split_score
                    best_attribute = attr
        
        return best_attribute
    
    def format_question(self, attribute):
        """Convert attribute to human-readable question"""
        question_map = {
            "gender": "Is your character male or female?",
            "universe": "What universe is your character from? (DC/Marvel/Other)",
            "has_powers": "Does your character have superpowers? (yes/no)",
            "is_hero": "Is your character a hero? (yes/no)", 
            "wears_mask": "Does your character wear a mask? (yes/no)",
            "human": "Is your character human? (yes/no)"
        }
        return question_map.get(attribute, f"What is your character's {attribute}?")
    
    def make_guess(self):
        """Make a guess based on remaining possibilities"""
        if len(self.current_possibilities) == 1:
            return self.current_possibilities[0]['name']
        elif len(self.current_possibilities) <= 3:
            # If few possibilities left, guess the most likely one
            return random.choice(self.current_possibilities)['name']
        return None
    
    def add_new_character(self):
        """Add a new character to the database"""
        print("\nI don't know this character! Help me learn.")
        name = input("What is your character's name? ").strip()
        
        new_character = {"name": name}
        
        # Ask about each attribute we track
        attributes = ["gender", "universe", "has_powers", "is_hero", "wears_mask", "human"]
        for attr in attributes:
            question = self.format_question(attr)
            answer = input(f"{question} ").strip().lower()
            new_character[attr] = answer
        
        self.characters.append(new_character)
        save_data(self.characters)
        print(f"Thanks! I've learned about {name}.")
    
    def play_again(self):
        """Reset the game for another round"""
        self.current_possibilities = self.characters.copy()
        self.questions_asked = []

def main():
    game = Akinator()
    
    while True:
        print("\n" + "="*50)
        print("Welcome to Terminal Akinator!")
        print("Think of a fictional comic character and I'll try to guess it!")
        print("Answer with the exact format requested (e.g., 'yes'/'no', 'male'/'female')")
        print("="*50)
        
        # Reset game for new round
        game.play_again()
        
        while len(game.current_possibilities) > 1:
            # Get the best question to ask
            attribute = game.get_best_question()
            
            if not attribute:
                break
                
            # Ask the question
            question = game.format_question(attribute)
            print(f"\n{question}")
            
            answer = input("Your answer: ").strip().lower()
            
            # Filter characters based on answer
            before_count = len(game.current_possibilities)
            game.filter_characters(attribute, answer)
            game.questions_asked.append(attribute)
            
            after_count = len(game.current_possibilities)
            print(f"Narrowed down from {before_count} to {after_count} possibilities")
            
            # If we're down to a few characters, try to guess
            if len(game.current_possibilities) <= 1:
                break
        
        # Make final guess
        if len(game.current_possibilities) == 1:
            guess = game.current_possibilities[0]['name']
            print(f"\nIs your character {guess}?")
            correct = input("Am I right? (yes/no): ").strip().lower()
            
            if correct == 'yes':
                print(" Great! I guessed it! 🎉")
            else:
                game.add_new_character()
        elif len(game.current_possibilities) == 0:
            print("\nI couldn't find any matching characters!")
            game.add_new_character()
        else:
            # Multiple possibilities left, make best guess
            print(f"\nI have {len(game.current_possibilities)} possibilities left:")
            for char in game.current_possibilities[:3]:  # Show top 3
                print(f"- {char['name']}")
            
            guess = random.choice(game.current_possibilities)['name']
            print(f"\nMy best guess is: {guess}")
            correct = input("Am I right? (yes/no): ").strip().lower()
            
            if correct == 'yes':
                print(" Lucky guess! ")
            else:
                print("Let me learn about your character...")
                game.add_new_character()
        
        # Ask if they want to play again
        play_again = input("\nWant to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break
    
    print("Thanks for playing Terminal Akinator! 👋")

if __name__ == "__main__":
    main()
