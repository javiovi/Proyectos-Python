from random import randint

choice = ["rock","paper","scissors"]
def main():
    computer = choice[randint(0,2)]


    print("Welcome to the Rock, Paper Scissors Game!")
    player = input("Your Choice: ").lower()
    print("Computer Chose: " + computer)


    if player == computer:
       print("Draw")
    elif player == "rock" and computer == "paper":
       print("Computer Wins")
    elif player == "rock" and computer == "scissors":
       print("Player Wins")
    elif player == "paper" and computer == "rock":
       print("Player Wins")
    elif player == "paper" and computer == "scissors":
       print("Computer Wins!")
    elif player == "scissors" and computer == "rock":
       print("Computer Wins")
    elif player == "scissors" and computer == "paper" :    
       print("Player Wins")

    main()

main()


