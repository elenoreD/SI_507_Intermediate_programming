from random import randrange
import random
## CONSTANTS ##

##Art by Hayley Jane Wakenshaw - https://www.asciiart.eu/animals/dogs
DOG_LEFT = """
   __
o-''|\_____/)
 \_/|_)     )
    \  __  /
    (_/ (_/ 
"""

DOG_RIGHT = """
        __
(\_____/|''-o
(     (_|\_/
 \  __   / 
  \_) \_) 
"""

##Art by Joan Stark - https://www.asciiart.eu/animals/cats
CAT_LEFT = """
 /\    /    
(' )  (
 (  \  )
 |(__)/
"""

CAT_RIGHT = """
\    /\\
 )  ( ')
(  /  )
 \(__)|
"""

class Pet:
    '''A Tamagotchi pet!
    Attributes
    ----------
    name : string
        The pet's name
    sound : 
        The pet's sound
    '''
    max_boredom = 6
    max_hunger = 10
    leaves_hungry = 16
    leaves_bored = 12

    ascii_art_left = ""
    ascii_art_right = ""

    # TODO: Add attribute "sound"
    def __init__(self, name,sound):
        self.name = name
        self.sound = sound
        self.hunger = randrange(self.max_hunger)
        self.boredom = randrange(self.max_boredom)
        self.tries=3

    def mood(self):
        '''Get the mood of a pet. A pet can be happy, hungry or bored,
        depending on wether it was fed or has played enough.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The mood of the pet
        '''

        if self.hunger <= self.max_hunger and self.boredom <= self.max_boredom:
            return "happy"
        elif self.hunger > self.max_hunger:
            return "hungry"
        else:
            return "bored"

    def status(self):
        '''Get the status of a pet to know it's name, how it feels and what it wants.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The name, mood and wants of the pet.
        '''

        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Please feed me.'
        if self.mood() == 'bored':
            state += 'You can play with me.'
        return state

    def do_command(self, resp):
        '''Calls the appropriate methods of a pet based on command "resp" given by player.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        '''

        if resp == "speak":
            print(self.speak())
        elif resp == "play":
            self.play()
        elif resp == "feed":
            self.feed()
        elif resp == "wait":
            print("Nothing to do...")
        else:
            print("Please provide a valid command.")


    def has_left(self):
        '''Returns True if a pet has left the game due to hunger or boredom, otherwise False.

        Parameters
        ----------
        none

        Returns
        -------
        bool
            If a pet has left
        '''

        return self.hunger > self.leaves_hungry or self.boredom > self.leaves_bored

    def clock_tick(self):
        '''Everytime call clock_tick function, hunger value increases 2, boredom value increases 2.

        Parameters
        ----------
        none

        Returns
        -------
        none

        '''

        self.hunger += 2
        self.boredom += 2

    def speak(self):
        '''Pet will speak the sound in certain ways.

        Parameters
        ----------
        none

        Returns
        -------
        string
        
        '''

        return 'I say: ' + self.sound

    def feed(self):
        '''Hunger decreases 5 when the function being called, and when the hunger value being negative, it will be set to 0 instead.

        Parameters
        ----------
        none

        Returns
        -------
        none
        
        '''

        self.hunger -= 5
        if self.hunger < 0:
            self.hunger = 0

    def play(self):
        '''The function is one of the commands, and might change the boredom value.
        
        When function being called, user will be asked to guess directions by inputing left or right, when user makes correct guess, boredom value increases 5, if the guess is wrong, function will show certian string and ask the user to try again. User can have 3 tries to guess, if all guesses are wrong, the boredom value will remain same. When user enter value besides left or right, function will remind user to revise the input.

        Parameters
        ----------
        none

        Returns
        -------
        none
        
        '''

        print('Guess which way I am looking at?')
        
        counter = 0
        while counter < self.tries:
            direction = random.choice(['right','left'])
            guess = input()
            if guess in ['right','left']:
                if guess == direction:
                    print('Correct!')
                    self.boredom -= 5
                    if self.boredom < 0:
                        self.boredom = 0
                    break
                elif direction == 'left':
                    print(self.ascii_art_left)
                    print('I look at', direction, ', Try again')
                    counter += 1
                else:
                    print(self.ascii_art_right)
                    print('I look at', direction, ', Try again')
                    counter += 1
            else:
                print("Only 'left' and 'right' are valid guesses. Try again.")
 

#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################

# TODO: Implement the Dog, Cat and Poodle subclasses and add docstrings

class Dog(Pet):
    '''Sub-class of Pet Class, certain functions will be modified.

    Parameters
    ----------
    Dog's name

    Returns
    -------
    Dog's sound
    
    '''

    ascii_art_left = DOG_LEFT
    ascii_art_right = DOG_RIGHT

    def speak(self):
        '''Dog will speak the sound in certain ways.

        Parameters
        ----------
        none

        Returns
        -------
        string
        
        '''
    
        return 'I say: ' + self.sound + 'arrrf!'
        
    def do_command(self, resp):
        '''Overwrite wait command of a pet based on command "resp" given by player.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        '''

        if resp == "wait":
            print("Please provide a valid command.")
        else:
            Pet.do_command(self,resp)

        
class Cat(Pet):
    '''Sub-class of Pet Class, certain functions will be modified.

    Parameters
    ----------
    Cat's name

    Returns
    -------
    Cat's sound
    
    '''

    ascii_art_left = CAT_LEFT
    ascii_art_right = CAT_RIGHT

    def __init__(self, name, sound,meow_count):
        '''Add one more attribute to cat class to change the speak function

        Parameters
        ----------
        none

        Returns
        -------
        none
        '''
        super().__init__(name,sound*meow_count)
        self.tries = 5
        
class Poodle(Dog):
    '''Sub-class of Dog Class, certain functions will be modified.

    Parameters
    ----------
    Dog's name

    Returns
    -------
    Dog's sound
    
    '''

    def dance(self):
        '''print a string.

        Parameters
        ----------
        none

        Returns
        -------
        none
        
        '''
        print("Dancing in circles like poodles do!")

    def do_command(self, resp):
        '''Change/modify certain new commands for Poodle.

        Parameters
        ----------
        resp : string
            The command to be issued to the pet.

        Returns
        -------
        none
        
        '''

        if resp == 'speak':
            self.dance()
            self.speak()
        elif resp == 'dance':
            self.dance()
        else:
            Dog.do_command(self,resp)

    

def get_name():
    '''Asks the player which name a pet should have.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("How do you want to name your pet?\n")
def get_sound():
    '''Asks the player what sound a pet should make

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    return input("What does your pet say?\n")
def get_meow_count():
    '''Asks the player how often a cat should make a sound.

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    while True:
        resp = input("How often does your Cat make a sound?\n")
        if resp.isnumeric():
            return int(resp)

p = None

while p == None:
    resp_pet_type = input("What kind of pet would you like to adopt?\n")
    resp_pet_type = resp_pet_type.lower()
    if resp_pet_type in ['dog', 'cat', 'poodle']:
        if resp_pet_type == 'dog':
            p = Dog(get_name(), get_sound())
        if resp_pet_type == 'cat':
            p = Cat(get_name(), get_sound(), get_meow_count())
        if resp_pet_type == 'poodle':
            p = Poodle(get_name(), get_sound())
        break
    else:
        print("We only have Cats, Dogs and Poodles.")


while not p.has_left():
    print()
    print(p.status())

    command = input("What should I do?\n")
    p.do_command(command)
    p.clock_tick()

print("Your pet has left.")