import unittest
import hw4_cards_ec1 as hands
import hw4_cards as cards

class TestCard(unittest.TestCase):
    
    def testAddAndRemove(self):
        hand = hands.Hand([])
        hand_len = len(hand.init_cards)
        card = cards.Card()
        hand.add_card(card)
        add_len = len(hand.init_cards)
        self.assertEqual(add_len-hand_len, 1)

        remcard = hand.remove_card(card)
        rem_len = len(hand.init_cards)
        if remcard is None:
            self.assertEqual(rem_len, add_len)
        else:
            self.assertEqual(rem_len+1, add_len)

    def testDraw(self):
        hand = hands.Hand([])
        hand_len = len(hand.init_cards)
        deck = cards.Deck()
        deck_len = len(deck.cards)
        hand.draw(deck)
        draw_deck_len = len(deck.cards)
        draw_hand_len = len(hand.init_cards)
        self.assertEqual(deck_len-draw_deck_len, 1)
        self.assertEqual(hand_len+1, draw_hand_len)

    


if __name__ == "__main__":
    unittest.main()