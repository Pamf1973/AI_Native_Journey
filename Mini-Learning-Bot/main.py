from bot.quiz import run_quiz
from bot.data_manager import add_word_menu

if __name__ == "__main__":
    while True:
        choice = input("\nChoose an option:\n1) Quiz\n2) Add word\n3) Quit\n> ").strip()
        if choice == "1":
            run_quiz()
        elif choice == "2":
            add_word_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please choose 1, 2, or 3.")
