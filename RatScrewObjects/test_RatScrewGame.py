import pytest
from CardDeckObjects import CardDeck
from RatScrewObjects.RatScrewGame import RatScrewGame
from RatScrewObjects.RatScrewPlayer import RatScrewPlayer


class TestRatScrewGame:
    """
    Test functionality of RatScrewGame class.
    """

    def test_reset_game_parameters(self):
        """
        Test reset_game_parameters method of RatScrewGame.
        """
        game = RatScrewGame()
        # Modify game parameters to be set to None to ensure reset works
        game.play_keys = None
        game.slap_keys = None
        game.players = None
        game.card_stack = None

        # Reset game parameters
        game.reset_game_parameters()

        # Check that game parameters are reset to initial states
        assert game.play_keys == dict() and isinstance(game.play_keys, dict)
        assert game.slap_keys == dict() and isinstance(game.slap_keys, dict)
        assert game.players == list() and isinstance(game.players, list)
        assert isinstance(game.card_stack, CardDeck) and game.card_stack.nCards == 52

    def test_get_number_of_players(self, monkeypatch):
        """
        Test get_number_of_players method of RatScrewGame.
        """
        game = RatScrewGame()

        # sequence of user inputs: invalid input followed by valid input
        user_inputs = ["foo", "3"]
        inputs = iter(user_inputs)

        # Patch the built-in 'input' function to use the iterator
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        n_players = game.get_number_of_players()
        assert n_players == 3

    def test_setup_game_with_too_many_players(self):
        """
        Test setup_game method of RatScrewGame when too many players are provided.
        """
        game = RatScrewGame()
        # Test with more than 52 players
        with pytest.raises(ValueError):
            game.setup_game(53)

    def test_setup_game_with_valid_number_of_players(self, monkeypatch):
        """
        Test setup_game method of RatScrewGame with a valid number of players.
        """
        game = RatScrewGame()
        n_players = 3
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d", "e", "f"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Check that the correct number of players have been added
        assert len(game.players) == n_players

        # Check that play and slap key dictionaries point to the correct player index
        for p_idx, player in enumerate(game.players):
            assert game.play_keys[player.play_key] == p_idx
            assert game.slap_keys[player.slap_key] == p_idx

        # Check that the card stack has been distributed among players
        total_player_cards = sum(player.card_stack.nCards for player in game.players)
        assert 52 == total_player_cards + game.card_stack.nCards

    def test_check_for_winner(self, monkeypatch):
        """
        Test check_for_winner method of RatScrewGame.
        """
        game = RatScrewGame()
        n_players = 3
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d", "e", "f"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Initially, there should be no winner
        assert game.check_for_winner() is None

        # Give all cards to player 1 and check for winner
        game.players[0].card_stack = CardDeck(nDecks=1)
        for p_idx in range(1, n_players):
            game.players[p_idx].card_stack = CardDeck(nDecks=0)

        assert game.check_for_winner() == 0

    def test_play_game(self, monkeypatch):
        """
        Provide test coverage for play_game method of RatScrewGame with a single player so only one round is played.
        """
        game = RatScrewGame()
        # Patch the built-in 'input' function to provide unique keys for each player and number of players
        user_inputs = iter(
            [
                "1",  # number of players
                "a",  # player 1 play key
                "b",  # player 1 slap key
            ]
        )
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        # Play game (will exit after one round since only one player)
        game.play_game()

    def test_play_round(self, monkeypatch):
        """
        Test play_round method of RatScrewGame.
        """
        game = RatScrewGame()
        n_players = 3
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d", "e", "f"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        starting_player = 1
        next_starting_player = game.play_round(starting_player)

        # Since play_round is a placeholder that always returns 0, check that
        # TODO: When play_round is fully implemented, can instead run this test by having a two person game where
        #       someone does penality slaps will they have no cards (round and game will be over at that point)
        assert next_starting_player == 0
