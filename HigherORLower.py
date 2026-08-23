import random as r

#Hello, this is a simple Higher or Lower game I made.
#I made this to refresh my mind on Python's syntax, with the help of Claude AI.
#I will be creating more simple programs, with the slight help of AI.
#After that, I'll try not to get help from AI, and will only rely on my previous small projects.
#Note to self: Try not to code too long, or you'll ultimately rely on AI xD.

class HigherORLower:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
    #secret_number - randomized number to be guessed
    #user_number - user's input
    #max_attempt - no. of attempts before losing
    #user_counter - user's no. of attempts
        self.secret_number = r.randint(1, 99)
        self.user_number = 0
        self.max_attempt = 10
        self.user_counter = 0
        self.user_input = ""
    
    def guess_number(self):
    #asks user for number
    #stores the user's guess
    #validates user input if its a number
    #increments user_counter every attempt
    #also shows user's attempt
        while True:
            try:
                self.user_number = int(input((f"Attempt {self.user_counter + 1} of {self.max_attempt}: Please enter a number: ")))
                if self.user_number > 99 or self.user_number < 1:
                    print("Please enter a number from 1-99 only.\n")
                    continue
                self.user_counter += 1
                break
            except ValueError:
                print("\nInput only accepts integers. Try again.")
        

    def check_if_won(self):
    #checks if the user correctly guessed
    #returns true or false
        return self.user_number == self.secret_number

    def check_attempt(self):
    #checks the user's remaining attempts
    #returns true or false
        return self.user_counter == self.max_attempt

    def play_again(self):
    #checks if user wants to play again
    #returns to play method if user inputs "y"
        user_input = ""
        while True:
            user_input = input("\nDo you want to play again? (y/n): ").lower()
            if user_input in ["y", "n"]:
                break
            print("/nInput only accepts y/n.")
        return user_input == "y"
    
    def play(self):
        #main method
        wants_to_continue = ""
        
        print("|HIGHER?          or                  |")
        print("|                              lower? |")
        print(" ")
        print("Guess the number ranging from 1-99")
        print("You only have 10 attempts. Good luck!")
        print(" ")
        
        while True:
            #resets the secret number and the user attempts for another game
            self.reset_game()
            while True:
                #calls the guess_number method
                self.guess_number()
                
                #checks if user_number is equal to secret_number
                #asks if user wants to play again through wants_to_continue variable
                if self.check_if_won():
                    print(f"\nYou won! The number was {self.secret_number}.")
                    wants_to_continue = self.play_again()
                    break
                #checks if user_counter exceeds max_attempt
                #asks if user wants to play again through wants_to_continue variable
                elif self.check_attempt():
                    print(f"\nNice try. The number was {self.secret_number}.")
                    wants_to_continue = self.play_again()
                    break
                else:
                    #checks user_number if its higher or lower than secret_number
                    if self.user_number > self.secret_number:
                        print("The number is lower.\n")
                    else:
                        print("The number is higher.\n")
            if not wants_to_continue:
                print("\n| Thank you for playing! |")
                break

#calls the HigherORLower class
#game.play() starts the game
game = HigherORLower()
game.play()