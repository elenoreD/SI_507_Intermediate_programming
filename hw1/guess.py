import random

secret = random.randint(0, 1000)
response = input("Enter a guess: ")
if int(response) == secret:
  print("You got it!")
else:
  print("Nope, you're wrong.")

  


