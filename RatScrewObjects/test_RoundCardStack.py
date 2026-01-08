import pytest
from CardDeckObjects import Card
from RatScrewObjects.RoundCardStack import RoundCardStack


class TestRoundCardStack:
    """
    Test functionality of RoundCardStack class.
    """

    def test_add_played_card_face_card(self):
        """
        Test add_played_card method when a face card is played.
        """
        stack = RoundCardStack()
        face_card = Card("jack", "hearts")
        stack.add_played_card(face_card)
        assert stack.need_face_card is True
        assert stack.face_card_countdown == 1  # Jack allows 1 chance
        assert stack.played_card_stack.nCards == 1
        assert stack.penalty_card_stack.nCards == 0

    def test_add_played_card_non_face_card(self):
        """
        Test add_played_card method when a non-face card is played.
        """
        countdown_default = 0
        stack = RoundCardStack()
        assert stack.face_card_countdown == countdown_default
        non_face_card = Card("7", "clubs")
        stack.add_played_card(non_face_card)
        assert stack.need_face_card is False
        assert stack.face_card_countdown == countdown_default - 1
        assert stack.played_card_stack.nCards == 1
        assert stack.penalty_card_stack.nCards == 0

    def test_add_penalty_card(self):
        """
        Test add_penalty_card method.
        """
        stack = RoundCardStack()
        penalty_card = Card("king", "spades")
        stack.add_penalty_card(penalty_card)
        assert stack.penalty_card_stack.nCards == 1
        assert stack.played_card_stack.nCards == 0
        # check that face card countdown and need_face_card remain unchanged
        assert stack.need_face_card is False
        assert stack.face_card_countdown == 0

    def test_has_stack_been_won(self):
        """
        Test has_stack_been_won method.
        """
        stack = RoundCardStack()
        # Initially, stack should not be won
        assert stack.has_stack_been_won() is False

        # Simulate playing a face card and countdown reaching zero
        face_card = Card("queen", "diamonds")
        stack.add_played_card(face_card)
        stack.face_card_countdown = 0  # Manually set countdown to 0
        assert stack.has_stack_been_won() is True

        # Reset and test when countdown is still positive
        stack = RoundCardStack()
        stack.add_played_card(face_card)
        assert stack.has_stack_been_won() is False

    def test_is_valid_slap_double(self):
        """
        Test is_valid_slap method for valid double.
        """
        stack = RoundCardStack()
        # Initially, slap should be invalid
        assert stack.is_valid_slap() is False

        double_val = "5"
        # Add two cards that are not the same to make slap invalid
        stack.add_played_card(Card("3", "clubs"))
        stack.add_played_card(Card(double_val, "diamonds"))
        assert stack.is_valid_slap() is False
        # Add card with the same value as the last card to make a double
        stack.add_played_card(Card(double_val, "hearts"))
        assert stack.is_valid_slap() is True

    def test_is_valid_slap_sandwich(self):
        """
        Test is_valid_slap method for valid sandwich.
        """
        stack = RoundCardStack()
        # Initially, slap should be invalid
        assert stack.is_valid_slap() is False

        sandwich_val = "9"
        # Add three cards that don't make a sandwich
        stack.add_played_card(Card("7", "clubs"))
        stack.add_played_card(Card(sandwich_val, "hearts"))
        stack.add_played_card(Card("2", "diamonds"))
        assert stack.is_valid_slap() is False

        # Add card with the same value as the second card to make a sandwich
        stack.add_played_card(Card(sandwich_val, "spades"))
        assert stack.is_valid_slap() is True
