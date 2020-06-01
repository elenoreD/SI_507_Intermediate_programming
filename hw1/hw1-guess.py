import random, math

secret = random.randint(0, 1000)
# print(secret)
while True:
  setup=input("Set a max value for secret number ")
  if setup.isnumeric():
    maxnumber=round(math.log((setup, 2))+1) 
    break
  else:
    print('Your max value should be an integer that is greater than zero')
  
count=0
while True:
  response = input("Enter a guess. or 'quit': ")
  if response.isnumeric() and int(response) in range(1,1000):
      num = int(response)
      if count<maxnumber:
        if num> secret:
          print('Too high! Try again.')
        if num < secret:
          print('Too low! Try again.') 
        if num == secret:
          print("You got it!")
          break
        count=count+1
        print('You have', maxnumber-count, 'more tries')
      else:
        print('You lose the game, the secret number is', secret)
        break
  elif response == 'quit':
    exit()
  else:
    print("Invalid input. Enter a number between 0 and 1000")




