import pytest

from CardDeckObjects import Card
from RatScrewObjects.RatScrewPlayer import RatScrewPlayer


class TestRatScrewPlayer:
    """
    Test functionality of RatScrewPlayer class.
    """

    def test_is_valid_action_key_with_no_constraints(self):
        """
        Test is_valid_action_key static method of RatScrewPlayer when constraints are not applied for which keys are invalid.
        """
        # Test with no constraints on which keys are invalid
        assert RatScrewPlayer.is_valid_action_key("a") is True
        assert RatScrewPlayer.is_valid_action_key("ab") is False

    def test_is_valid_action_key_with_constraints(self):
        """
        Test is_valid_action_key static method of RatScrewPlayer when constraints are applied for which keys are invalid.
        """

        # Test with constraints on which keys are invalid
        invalid_keys = {"x", "y", "z"}
        assert RatScrewPlayer.is_valid_action_key("x", invalid_keys) is False
        assert RatScrewPlayer.is_valid_action_key("a", invalid_keys) is True
        assert RatScrewPlayer.is_valid_action_key("yz", invalid_keys) is False
        assert RatScrewPlayer.is_valid_action_key("bc", invalid_keys) is False

    def test_init(self, monkeypatch, invalid_action_keys=None):
        """
        Test initialization of RatScrewPlayer.
        """

        # sequence of user inputs for play and slap keys, invalid input followed by valid input
        user_inputs = ["foo", "a", "bar", "b"]
        inputs = iter(user_inputs)

        # Patch the built-in 'input' function to use the iterator
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        player = RatScrewPlayer(invalid_action_keys)
        assert player.play_key == user_inputs[1]
        assert player.slap_key == user_inputs[3]
        assert player.card_stack.nCards == 0

    def test_init_with_existing_invalid_keys(self, monkeypatch):
        """
        Add test coverage for initialization of RatScrewPlayer with existing invalid action keys.
        """
        # pre-existing invalid keys that will be checked against during initialization
        existing_invalid_keys = {"x", "y", "z"}
        # rerun the init test with these existing invalid keys
        self.test_init(monkeypatch, existing_invalid_keys)

    def test_play_card_no_cards(self, monkeypatch):
        """
        Test playing a card when player has no cards.
        """
        # sequence of user inputs for play and slap keys, invalid input followed by valid input
        user_inputs = ["foo", "a", "bar", "b"]
        inputs = iter(user_inputs)

        # Patch the built-in 'input' function to use the iterator
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        player = RatScrewPlayer()
        with pytest.raises(IndexError):
            player.play_card()

    def test_play_card_valid(self, monkeypatch):
        """
        Test playing a card when player has no cards.
        """
        # sequence of user inputs for play and slap keys, invalid input followed by valid input
        user_inputs = ["foo", "a", "bar", "b"]
        inputs = iter(user_inputs)

        # Patch the built-in 'input' function to use the iterator
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        player = RatScrewPlayer()
        expected_card = Card("5", "hearts")
        player.card_stack.add_card(expected_card)
        assert player.play_card() == expected_card
