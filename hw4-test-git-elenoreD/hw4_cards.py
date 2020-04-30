import random
import hw4_cards_ec2 as hw



# SI 507 Winter 2020
# Homework 4 - Code

######### DO NOT CHANGE IN THE MAIN ASSIGNMENT #########

class Card:
    '''a standard playing card

    cards will have a suit and a rank

    Class Attributes
    ----------------
    suit_names: list
        the four suit names in order 
        0:Diamonds, 1:Clubs, 2: Hearts, 3: Spades
    
    faces: dict
        maps face cards' rank name
        1:Ace, 11:Jack, 12:Queen,  13:King

    Instance Attributes
    -------------------
    suit: int
        the numerical index into the suit_names list

    suit_name: string
        the name of the card's suit

    rank: int
        the numerical rank of the card

    rank_name: string
        the name of the card's rank (e.g., "King" or "3")

    '''
    suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
    faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

    def __init__(self, suit=0,rank=2):
        self.suit = suit
        self.suit_name = Card.suit_names[self.suit]

        self.rank = rank
        if rank in Card.faces:
            self.rank_name = Card.faces[self.rank]
        else:
            self.rank_name = str(self.rank)

    def __str__(self):
        return f"{self.rank_name} of {self.suit_name}"


class Deck:
    '''a deck of Cards

    Instance Attributes
    -------------------
    cards: list
        the list of Cards currently in the Deck. Initialized to contain
        all 52 cards in a standard deck

    ''' 
    def __init__(self): 
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card)
   
    def deal_card(self, i=-1):
        '''remove a card from the Deck

        Parameters  
        -------------------
        i: int (optional)
            the index of the ard to remove. Default (-1) will remove the "top" card

        Returns
        -------
        Card
            the Card that was removed

        '''
        return self.cards.pop(i) 

    def shuffle(self):
        '''shuffles (randomizes the order) of the Cards

        self.cards is modified in place

        Parameters  
        ----------
        None

        Returns
        -------
        None

        '''
        random.shuffle(self.cards)

    def sort_cards(self):
        '''returns the Deck to its original order
        
        Cards will be in the same order as when Deck was constructed.
        self.cards is modified in place.

        Parameters  
        ----------
        None

        Returns
        -------
        None

        '''
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card)

    def replace_card(self, card):
        '''replace a card to the Deck
        when the card is not in the Deck, add the card
        when the card is in the Deck, ignore the card

        Parameters  
        -------------------
        card: instance
            an instance of a card to replace

        Returns
        -------
        None

        '''
        
        for c in self.cards:
            if c.rank == card.rank and c.suit == card.suit:
                return

        self.cards.append(card)

    def deal(self, number_of_hands, number_of_cards_per_hand):
        '''Takes two parameters representing the number of hands and the number of cards per hand
         returns a list of Hands 

        Parameters  
        -------------------
        number_of_hands: int
            an integer shows number of hands
        number_of_cards_per_hand: int
            an integer shows number of cards per hand


        Returns
        -------
        hands: list
            a list of hands 

        '''

        hand_list = []
        distribute = {}
        self.shuffle()
        for n in range(52):
            if (n % number_of_hands) not in distribute:
                distribute[n % number_of_hands] = [self.cards[n]]
            else:
                distribute[n % number_of_hands].append(self.cards[n])
        # to distribute deck normally

        for modulo in distribute:
            if number_of_cards_per_hand != -1:
                hand_list.append(hw.Hand(distribute[modulo][0:number_of_cards_per_hand]))
            else:
                hand_list.append(hw.Hand(distribute[modulo]))
        
        return hand_list


        # 1. too many hands
        # 2. not evenly distributed : a)cards -1,b) number_of_hands*number_of_cards_per_hand>52
        


if __name__ == "__main__":
    pass

