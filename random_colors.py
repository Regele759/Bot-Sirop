import random
import sys

# Define a list of colors with their hex codes and ANSI color codes
COLORS = {
    "red": ("\033[91m", "#FF0000"),
    "green": ("\033[92m", "#00FF00"),
    "yellow": ("\033[93m", "#FFFF00"),
    "blue": ("\033[94m", "#0000FF"),
    "magenta": ("\033[95m", "#FF00FF"),
    "cyan": ("\033[96m", "#00FFFF"),
    "white": ("\033[97m", "#FFFFFF"),
    "orange": ("\033[38;5;208m", "#FFA500"),
    "purple": ("\033[38;5;135m", "#800080"),
    "pink": ("\033[38;5;205m", "#FFC0CB"),
    "lime": ("\033[38;5;154m", "#00FF00"),
    "navy": ("\033[38;5;17m", "#000080"),
}

RESET = "\033[0m"


def get_random_color():
    """Returns a random color from the COLORS dictionary"""
    return random.choice(list(COLORS.items()))


def display_random_colors(count=5):
    """Display random colors"""
    print("\n" + "="*50)
    print("🎨 RANDOM COLOR GENERATOR 🎨")
    print("="*50 + "\n")
    
    for i in range(count):
        color_name, (ansi_code, hex_code) = get_random_color()
        print(f"{ansi_code}● {color_name.upper():12} | Hex: {hex_code}{RESET}")
    
    print("\n" + "="*50 + "\n")


def interactive_mode():
    """Interactive mode - press Enter to generate random colors"""
    print("\n" + "="*50)
    print("🎨 INTERACTIVE COLOR GENERATOR 🎨")
    print("="*50)
    print("Press Enter to generate random colors, or type 'quit' to exit\n")
    
    while True:
        user_input = input("Enter command (or press Enter for random colors): ").strip().lower()
        
        if user_input == 'quit' or user_input == 'exit':
            print("\n👋 Thanks for using Color Generator!\n")
            break
        else:
            # Any other command generates random colors
            display_random_colors()


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # If argument provided, generate that many colors
        try:
            count = int(sys.argv[1])
            display_random_colors(count)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid number")
            sys.exit(1)
    else:
        # Default: interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
