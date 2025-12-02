import pytest

from CardDeck.Card import Card


class TestCard:
    """
    Test functionality of the Card class.
    """

    def test_card_creation(self):
        """
        Test creating a valid card.
        """
        card = Card(value="2", suit="spades")
        assert card.value == "2"
        assert card.suit == "spades"

    def test_card_creation_not_case_sensitive(self):
        """
        Test creating a card with mixed case value and suit.
        """
        card = Card(value="qUeEn", suit="hEarts")
        assert card.value == "queen"
        assert card.suit == "hearts"

    def test_invalid_value(self):
        """
        Test that creating a card with an invalid value raises a ValueError.
        """
        with pytest.raises(ValueError):
            Card("11", "clubs")

    def test_invalid_suit(self):
        """
        Test that creating a card with an invalid suit raises a ValueError.
        """
        with pytest.raises(ValueError):
            Card("8", "stars")
