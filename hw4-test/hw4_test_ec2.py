import unittest
import hw4_cards_ec1 as hands
import hw4_cards as cards
import hw4_cards_ec2 as hands2

class TestCard(unittest.TestCase):

    def testRemovePair(self):
        card1 = cards.Card(suit=1, rank=2)
        card2 = cards.Card(suit=2, rank=2)
        card3 = cards.Card(suit=3, rank=3)
        cards_in_hand = [card1, card2, card3]
        hand = hands2.Hand(cards_in_hand)
        hand.remove_pairs()
        self.assertEqual(len(hand.init_cards),1)

    def testDealFuncion(self):
        # test name always start with 'test'
        deck = cards.Deck()
        hands_list = deck.deal(4,12)
        self.assertEqual(len(hands_list),4)
        self.assertEqual(len(hands_list[0].init_cards),12)
        self.assertEqual(len(hands_list[3].init_cards),12)
        hands_list2 = deck.deal(4,-1)
        self.assertEqual(len(hands_list2),4)
        self.assertEqual(len(hands_list2[0].init_cards),13)
        hands_list3 = deck.deal(7,9)
        self.assertEqual(len(hands_list3),7)
        self.assertEqual(len(hands_list3[0].init_cards),8)
        self.assertEqual(len(hands_list3[-1].init_cards),7)

if __name__ == "__main__":
    unittest.main()