import json
import random
import time
from colorama import init, Fore

# Initialize colorama to support coloured output
init(autoreset=True)

# Loading the quiz questions from JSON file
def load_questions(filename="quiz.json"):
    with open(filename, "r") as file:
        questions = json.load(file)
    return questions

# Saving the user's score to a file
def save_score(name, score, total):
    percentage = round((score / total) * 100, 2)
    result = {
        "name": name,
        "score": score,
        "total": total,
        "percentage": percentage
    }

    # Load scores
    try:
        with open("results.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(result)

    # Save all results back to the file
    with open("results.json", "w") as file:
        json.dump(data, file, indent=4)

# Ask one question and return True if correct, False otherwise
def ask_question(q, index):
    print(f"\nQuestion {index + 1}: {q['question']}")

    options = q['options']
    correct_option = options[q['answer'] - 1] 

    # Pair options with numbers and shuffle them
    option_map = list(enumerate(options, start=1))
    random.shuffle(option_map)

    # Find which number now corresponds to the correct answer
    for number, text in option_map:
        if text == correct_option:
            correct_number = number
            break

    # Show shuffled options
    for number, text in option_map:
        print(f"   {number}. {text}")

    # Get user input
    try:
        choice = int(input("Your answer (1-4): "))
        if choice == correct_number:
            print(Fore.GREEN + "✅ Correct!")
            return True
        else:
            print(Fore.RED + f"❌ Wrong! The correct answer was: {correct_option}")
            return False
    except ValueError:
        print(Fore.YELLOW + "That wasn't a valid number. No points for this one.")
        return False

# Run the whole quiz
def run_quiz():
    print(Fore.CYAN + "\n ==== Welcome to the Python Quiz Game ==== ")
    name = input("What's your name? ").strip()
    if not name:
        name = "Anonymous"

    questions = load_questions()
    random.shuffle(questions)

    score = 0
    total_questions = len(questions)

    print(Fore.CYAN + f"\nAlright {name}, let's begin!\n")

    for i, question in enumerate(questions):
        is_correct = ask_question(question, i)
        if is_correct:
            score += 1
        time.sleep(1)

    # Show final result
    print(Fore.MAGENTA + "\n ==== Quiz Completed! ====")
    print(Fore.BLUE + f"Player: {name}")
    print(Fore.BLUE + f"Score: {score}/{total_questions}")
    print(Fore.BLUE + f"Percentage: {round((score / total_questions) * 100, 2)}%")

    # Save result
    save_score(name, score, total_questions)

if __name__ == "__main__":
    run_quiz()