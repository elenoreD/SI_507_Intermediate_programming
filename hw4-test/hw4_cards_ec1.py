
# create the Hand with an initial set of cards
import hw4_cards as cards


class Hand:
    '''a hand for playing card

    Class Attributes
    ----------------
    None

    Instance Attributes
    -------------------
    init_card: list
        a list of cards

    '''
    def __init__(self, init_cards):
        #self.init_cards = init_cards
        self.init_cards = init_cards
        

    def add_card(self, card):
        '''add a card
        add a card to the hand
        silently fails if the card is already in the hand

        Parameters  
        -------------------
        card: instance
            a card to add

        Returns
        -------
        None

        '''
        if card not in self.init_cards:
            self.init_cards.append(card)


    def remove_card(self, card):
        '''remove a card from the hand

        Parameters  
        -------------------
        card: instance
            a card to remove

        Returns
        -------
        the card, or None if the card was not in the Hand

        '''
        if card in self.init_cards:
            self.init_cards.remove(card)
        else:
            card = None

        return card
 
    def draw(self, deck):
        '''draw a card
        draw a card from a deck and add it to the hand
        side effect: the deck will be depleted by one card

        Parameters  
        -------------------
        deck: instance
            a deck from which to draw

        Returns
        -------
        None

        '''
        card = deck.deal_card()
        self.add_card(card)
        

        
if __name__ == "__main__":
    pass


