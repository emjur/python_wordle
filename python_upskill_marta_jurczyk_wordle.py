import requests
from termcolor import colored
import random 

# random five-letter word from API definition

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
words = response.content.splitlines()
correct_word=""
while 1:
    correct_word = random.choice(words).decode()
    word_len = len(correct_word)
    if word_len == 5:
        break

#user input validation - if it is valid, english, five-letter, non-digit word:

def word_check(user_input):
    #five letter check
    if len(user_input)<5 or len(user_input)>5:
        print("\""+user_input+"\""+" is not five-letter! Try another one!")
        return False
    #digits check
    elif not user_input.isalpha():
        print("\""+user_input+ "\""+" contains digits! Try with valid five-letter one!")
        return False
    #word validness check
    else: 
        response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+user_input)
        if response.ok:
            return True
        else: 
            print("\""+user_input+ "\""+" is not a valid word!")
            return False

# creating an array - if letter is in right place: 2, letter in word but wrong position:1, letter not in the word: 0

def check_letters(correct_word,guess):
    answer_array=[]
    # [0, 1, 2, 1, 0]
    # 0 - bad letter
    # 1 - correct letter wrong position
    # 2 - correct letter correct position
    cwl_list=list(correct_word)
    guess_list=list(guess)
    for i in range(5):
        if cwl_list[i]==guess_list[i]:
            answer_array.append(2)
        elif guess[i] in correct_word:
            answer_array.append(1)
        else: answer_array.append(0)
    return answer_array

# printing user input colored based on guessed word array

def print_result(guess, answer_array):
    # 0 - red
    # 1 - yellow
    # 2 - green
    colors=["red","yellow","green"]
    for i, val in enumerate(answer_array):
        color=colors[val]
        print(colored(guess[i]+" ", color), end='')
    print("")


print("Guess valid five-letter word:")
print("If the letter is in correct place - GREEN")
print("If the letter is in incorrect place - YELLOW")
print("If the letter is not in the word - RED")

# user input and correct word comparison:

for i in range(5):
    user_input = input()
    while not word_check(user_input):
        user_input=input()
    answer_array = check_letters(correct_word, user_input)
    print_result(user_input, answer_array)
    if all(p == 2 for p in answer_array):
        print("You won!")
        print("Do you know what it means? Check this out!")
        word_def = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+correct_word)
        print(word_def.json()[0]["sourceUrls"][0])
        break
    print("Try another word!")

# when the word wasn not guessed - show it and the link to wiki: 
print("You lost! Next round?")    
print("Correct word was:"+correct_word)
word_def = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+correct_word)
print("Do you know what it means? Check this out!")
print(word_def.json()[0]["sourceUrls"][0])

            


