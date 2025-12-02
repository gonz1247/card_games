import pytest

from CardDeck.CardDeck import CardDeck
from CardDeck.Card import Card


class TestCardDeck:
    """
    Test functionality of the CardDeck class.
    """

    def test_unique_deck(self):
        """
        Test that a single deck contains 52 unique cards.
        """
        deck = CardDeck(nDecks=1)
        unique_cards = set((card.value, card.suit) for card in deck.cards)
        assert len(unique_cards) == deck.nCards == 52

    def test_deal_card_empty_deck(self):
        """
        Test dealing a card from an empty deck raises an error.
        """
        deck = CardDeck(nDecks=0)
        with pytest.raises(IndexError):
            deck.deal_card()

    def test_deal_card_from_bottom(self):
        """
        Test dealing a card from the bottom of the deck removes the expected card from the deck.
        """
        deck = CardDeck()
        initial_nCards = deck.nCards
        expected_card_suit = deck.cards[0].suit
        expected_card_value = deck.cards[0].value
        card = deck.deal_card(fromBottom=True)
        assert isinstance(card, Card)
        assert deck.nCards == initial_nCards - 1
        assert card.suit == expected_card_suit
        assert card.value == expected_card_value

    def test_deal_card_from_top(self):
        """
        Test dealing a card from the top of the deck removes the expected card from the deck.
        """
        deck = CardDeck()
        initial_nCards = deck.nCards
        expected_card_suit = deck.cards[-1].suit
        expected_card_value = deck.cards[-1].value
        card = deck.deal_card(fromBottom=False)
        assert isinstance(card, Card)
        assert deck.nCards == initial_nCards - 1
        assert card.suit == expected_card_suit
        assert card.value == expected_card_value

    def test_add_card_on_top(self):
        """
        Test adding a card on top of the deck.
        """
        deck = CardDeck()
        card = Card(value="5", suit="diamonds")
        initial_nCards = deck.nCards
        deck.add_card(card, onTop=True)
        assert deck.nCards == initial_nCards + 1
        assert deck.cards[-1] == card

    def test_add_card_on_bottom(self):
        """
        Test adding a card on bottom of the deck.
        """
        deck = CardDeck()
        card = Card(value="king", suit="clubs")
        initial_nCards = deck.nCards
        deck.add_card(card, onTop=False)
        assert deck.nCards == initial_nCards + 1
        assert deck.cards[0] == card

    def test_deal_deck(self):
        """
        Test dealing the deck into multiple piles gives even piles with unique instances of
        """
        deck = CardDeck(nDecks=0)
        nPiles = 2
        card1 = Card(value="7", suit="hearts")
        card2 = Card(value="ace", suit="spades")
        card3 = Card(value="10", suit="clubs")
        deck.add_card(card1)
        deck.add_card(card2)
        deck.add_card(card3)
        nCards = deck.nCards
        piles = deck.deal_deck(nPiles=nPiles)
        assert len(piles) == nPiles
        assert piles[0].nCards == piles[1].nCards
        total_cards_in_piles = piles[0].nCards * nPiles
        assert total_cards_in_piles + deck.nCards == nCards
        card1 = piles[0].deal_card()
        card2 = piles[1].deal_card()
        card3 = deck.deal_card()
        assert card1 is not card2
        assert card1 is not card3
        assert card2 is not card3
