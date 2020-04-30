
#########################################
##### Name: <Shengnan Duan>         #####
##### Uniqname:<elenore>            #####
#########################################

import unittest
import hw4_cards as cards

# SI 507 Winter 2020
# Homework 4 - Code

## You can write any additional debugging/trying stuff out code here...
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

class TestCard(unittest.TestCase):
    # this is a "test"
    def test_0_create(self):
        card = cards.Card()
        self.assertEqual(card.suit_name, "Diamonds")
        self.assertEqual(card.rank, 2)

    # Add methods below to test main assignments. 
    def test_1_queen(self):
        card = cards.Card(rank=12)
        self.assertEqual(card.rank_name, "Queen")

    def test_2_clubs(self):
        card = cards.Card(suit=1)
        self.assertEqual(card.suit_name, "Clubs")
    
    def test_3_str(self):
        card = cards.Card(3 , 13)
        self.assertEqual(card.__str__(), "King of Spades")
       
    def test_4_deck(self):
        deck = cards.Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_5_deal_card(self):
        deck = cards.Deck()
        deck.deal_card()
        self.assertIsInstance(deck, cards.Deck)

    def test_6_fewer(self):
        deck = cards.Deck()
        before_deal = len(deck.cards)
        deck.deal_card()
        after_deal = len(deck.cards)
        self.assertEqual(before_deal-after_deal, 1)

    def test_7_replace(self):
        deck = cards.Deck()
        card = deck.deal_card()
        no_replace = len(deck.cards)
        deck.replace_card(card)
        replace = len (deck.cards)
        self.assertEqual(replace-no_replace, 1)

    def test_8_replace(self):
        deck = cards.Deck()
        before_replace = len(deck.cards)
        for card in deck.cards:
            deck.replace_card(card)
        after_replace = len(deck.cards)
        self.assertEqual(before_replace - after_replace, 0)


############
### The following is a line to run all of the tests you include:
if __name__ == "__main__":
    unittest.main()
