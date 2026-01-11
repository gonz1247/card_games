import pytest
from CardDeckObjects import CardDeck, Card
from RatScrewObjects.RatScrewGame import RatScrewGame
from RatScrewObjects.RoundCardStack import RoundCardStack


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
        game.round_stack = None

        # Reset game parameters
        game.reset_game_parameters()

        # Check that game parameters are reset to initial states
        assert game.play_keys == dict() and isinstance(game.play_keys, dict)
        assert game.slap_keys == dict() and isinstance(game.slap_keys, dict)
        assert game.players == list() and isinstance(game.players, list)
        assert isinstance(game.round_stack, RoundCardStack)
        assert game.round_stack.played_card_stack.nCards == 0
        assert game.round_stack.penalty_card_stack.nCards == 0
        assert game.round_stack.need_face_card is False
        assert game.round_stack.face_card_countdown == 0

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

    def test_get_number_of_players_with_too_many_players(self, monkeypatch):
        """
        Test get_number_of_players method of RatScrewGame when too many players are provided.
        """
        game = RatScrewGame()

        # sequence of user inputs: invalid input (too many players) followed by valid input
        user_inputs = [str(game._MAX_PLAYERS + 1), "2"]
        inputs = iter(user_inputs)

        # Patch the built-in 'input' function to use the iterator
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        n_players = game.get_number_of_players()
        assert n_players == 2

    def test_setup_game_with_too_many_players(self):
        """
        Test setup_game method of RatScrewGame when too many players are provided.
        """
        game = RatScrewGame()
        # Test with more than max number of players
        with pytest.raises(ValueError):
            game.setup_game(game._MAX_PLAYERS + 1)

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
        assert (
            total_player_cards
            + game.round_stack.played_card_stack.nCards
            + game.round_stack.penalty_card_stack.nCards
            == game._MAX_CARDS
        )

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

        # Give all cards to player 0 and check for winner
        winner_player_idx = 0
        for p_idx in range(n_players):
            if p_idx == winner_player_idx:
                game.players[p_idx].card_stack = CardDeck(nDecks=1)
            else:
                game.players[p_idx].card_stack = CardDeck(nDecks=0)
        assert game.check_for_winner() == winner_player_idx

    def test_play_game(self, monkeypatch):
        """
        Provide test coverage for play_game method of RatScrewGame
        """
        game = RatScrewGame()
        # Patch the built-in 'input' function to provide unique keys for each player and number of players
        user_inputs = iter(
            [
                "2",  # number of players
                "a",  # player 1 play key
                "b",  # player 1 slap key
                "c",  # player 2 play key
                "d",  # player 2 slap key
            ]
        )
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

        # Override play_round and check_for_winner to end game after one round
        game.play_round = lambda starting_player: 0
        game.check_for_winner = lambda: 0

        # Run play_game method to provide test coverage
        game.play_game()

    def test_play_round(self, monkeypatch):
        """
        Test play_round method of RatScrewGame.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup cards for players so that can test round play
        starting_player = 0
        losing_player = 1
        game.players[starting_player].card_stack = CardDeck(nDecks=0)
        game.players[starting_player].card_stack.add_card(Card("jack", "hearts"))
        game.players[losing_player].card_stack = CardDeck(nDecks=0)
        game.players[losing_player].card_stack.add_card(Card("3", "spades"))

        # Add a card to the penalty stack
        game.round_stack.add_penalty_card(Card("7", "clubs"))

        # Patch the built-in 'input' function to force a sequence of plays
        user_inputs = iter(["a", "c"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

        # Play round where second player loses since they cannot play a face card
        next_starting_player = game.play_round(starting_player)
        assert next_starting_player == starting_player
        assert game.players[starting_player].card_stack.nCards == 3
        assert game.players[losing_player].card_stack.nCards == 0

    def test_get_next_elgible_player(self, monkeypatch):
        """
        Test _get_next_elgible_player method of RatScrewGame.
        """
        game = RatScrewGame()
        n_players = 4
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d", "e", "f", "g", "h"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Set players 1 and 2 to have no cards
        game.players[1].card_stack = CardDeck(nDecks=0)
        game.players[2].card_stack = CardDeck(nDecks=0)

        # Starting from player 0, the next elgible player should be player 3
        next_player = game._get_next_elgible_player(current_player_idx=0)
        assert next_player == 3

        # Starting from player 3, the next elgible player should be player 0
        next_player = game._get_next_elgible_player(3)
        assert next_player == 0

    def test_get_next_elgible_player_all_players_out(self, monkeypatch):
        """
        Test _get_next_elgible_player method of RatScrewGame when all players have no cards.
        """
        game = RatScrewGame()
        n_players = 4
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d", "e", "f", "g", "h"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Set all players to have no cards
        for p in game.players:
            p.card_stack = CardDeck(nDecks=0)

        # Since no one has cards, the next elgible player should be the current player
        for idx in range(n_players):
            next_player = game._get_next_elgible_player(current_player_idx=idx)
            assert next_player == idx

    def test_process_playing_card_lost_round(self, monkeypatch):
        """
        Test process_playing_card method of RatScrewGame when the player loses the round.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to require a face card to be played
        game.round_stack.need_face_card = True
        game.round_stack.face_card_countdown = 1

        # Override current player's card stack to have no face cards
        current_player_idx = 0
        game.players[current_player_idx].card_stack = CardDeck(nDecks=0)
        game.players[current_player_idx].card_stack.add_card(Card("2", "hearts"))

        # Test playing a card
        previous_player_idx = 1
        round_winner, player_turn_over = game.process_playing_card(
            current_player_idx=current_player_idx,
            previous_player_idx=previous_player_idx,
        )
        assert round_winner == previous_player_idx
        assert player_turn_over is True

    def test_process_playing_card_face_card_played(self, monkeypatch):
        """
        Test process_playing_card method of RatScrewGame when a face card is played.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to not require a face card to be played
        game.round_stack.need_face_card = False
        game.round_stack.face_card_countdown = 0

        # Override current player's card stack to have a face card
        current_player_idx = 0
        game.players[current_player_idx].card_stack = CardDeck(nDecks=0)
        game.players[current_player_idx].card_stack.add_card(Card("king", "hearts"))

        # Test playing a card
        previous_player_idx = 1
        round_winner, player_turn_over = game.process_playing_card(
            current_player_idx=current_player_idx,
            previous_player_idx=previous_player_idx,
        )
        assert round_winner is None  # no one should win the round
        assert player_turn_over is True  # since they played a face card

    def test_process_playing_card_turn_still_going(self, monkeypatch):
        """
        Test process_playing_card method of RatScrewGame when the current player can continue playing.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to require a face card to be played within two plays
        game.round_stack.need_face_card = True
        game.round_stack.face_card_countdown = 2

        # Override current player's card stack to have only one card
        current_player_idx = 0
        game.players[current_player_idx].card_stack = CardDeck(nDecks=0)
        game.players[current_player_idx].card_stack.add_card(Card("5", "hearts"))
        game.players[current_player_idx].card_stack.add_card(Card("9", "spades"))

        # Test playing a card
        previous_player_idx = 1
        round_winner, player_turn_over = game.process_playing_card(
            current_player_idx=current_player_idx,
            previous_player_idx=previous_player_idx,
        )
        assert round_winner is None  # player can still play
        assert player_turn_over is False  # since countdown has not reached zero

    def test_process_slapping_stack_valid_slap(self, monkeypatch):
        """
        Test process_slapping_stack method of RatScrewGame when it's a valid slap.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in a valid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("5", "spades"))

        # Test slapping the stack
        slapping_player_idx = 0
        current_player_idx = 1
        round_winner, player_turn_over = game.process_slapping_stack(
            slapping_player_idx=slapping_player_idx,
            current_player_idx=current_player_idx,
        )
        assert round_winner == slapping_player_idx
        assert player_turn_over is True

    def test_process_slapping_stack_invalid_slap_no_cards(self, monkeypatch):
        """
        Test process_slapping_stack method of RatScrewGame when an invalid slap is done by a player with no cards.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in an invalid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("6", "spades"))

        # Set slapping player to have no cards
        slapping_player_idx = 0
        game.players[slapping_player_idx].card_stack = CardDeck(nDecks=0)

        # Test slapping the stack
        current_player_idx = 1
        round_winner, player_turn_over = game.process_slapping_stack(
            slapping_player_idx=slapping_player_idx,
            current_player_idx=current_player_idx,
        )
        assert round_winner is None
        assert player_turn_over is False

    def test_process_slapping_stack_invalid_slap_with_cards(self, monkeypatch):
        """
        Test process_slapping_stack method of RatScrewGame when an invalid slap is done by a player with cards.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in an invalid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("6", "spades"))

        # Ensure slapping player has cards
        slapping_player_idx = 0
        game.players[slapping_player_idx].card_stack = CardDeck(nDecks=0)
        game.players[slapping_player_idx].card_stack.add_card(Card("9", "clubs"))
        expected_cards_after_penalty = (
            game.players[slapping_player_idx].card_stack.nCards - 1
        )

        # Test slapping the stack
        current_player_idx = 1
        round_winner, player_turn_over = game.process_slapping_stack(
            slapping_player_idx=slapping_player_idx,
            current_player_idx=current_player_idx,
        )
        assert round_winner is None
        assert player_turn_over is False
        assert (
            game.players[slapping_player_idx].card_stack.nCards
            == expected_cards_after_penalty
        )

    def test_process_slapping_stack_invalid_slap_by_current_player(self, monkeypatch):
        """
        Test process_slapping_stack method of RatScrewGame when an invalid slap is done by the current player.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in a invalid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("7", "spades"))

        # set current player to only have one card so they will have no cards after penalty
        slapping_player_idx = 0
        game.players[slapping_player_idx].card_stack = CardDeck(nDecks=0)
        game.players[slapping_player_idx].card_stack.add_card(Card("9", "clubs"))

        # Test slapping the stack by the current player
        round_winner, player_turn_over = game.process_slapping_stack(
            slapping_player_idx=slapping_player_idx,
            current_player_idx=slapping_player_idx,
        )
        assert round_winner is None
        assert player_turn_over is True

    def test_process_player_actions_card_played(self, monkeypatch):
        """
        Test process_player_actions method of RatScrewGame when a card is played.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        play_card_key = "a"
        user_inputs = iter([play_card_key, "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup player cards with a single known card
        current_player_idx = 0
        game.players[current_player_idx].card_stack = CardDeck(nDecks=0)
        played_card = Card("5", "hearts")
        game.players[current_player_idx].card_stack.add_card(played_card)

        # Test processing player actions
        previous_player_idx = 1
        round_winner, player_turn_over = game.process_player_actions(
            player_actions=play_card_key,
            current_player_idx=current_player_idx,
            previous_player_idx=previous_player_idx,
        )
        assert round_winner is None
        assert player_turn_over is True
        assert game.players[current_player_idx].card_stack.nCards == 0
        assert game.round_stack.played_card_stack.nCards == 1
        assert game.round_stack.penalty_card_stack.nCards == 0
        assert game.round_stack.played_card_stack.see_card(0) == played_card

    def test_process_player_actions_stack_slapped_multiple_attempts(self, monkeypatch):
        """
        Test process_player_actions method of RatScrewGame when attempted to be slapped multiple times by one person.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        slap_key = "b"
        user_inputs = iter(["a", slap_key, "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in a invalid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("6", "spades"))

        # Get expected number of cards after penalty
        slapping_player_idx = 0
        expected_cards_after_penalty = (
            game.players[slapping_player_idx].card_stack.nCards - 1
        )

        # Test slapping the stack
        current_player_idx = 1
        round_winner, player_turn_over = game.process_player_actions(
            player_actions=slap_key * 3,  # multiple slap attempts
            current_player_idx=current_player_idx,
            previous_player_idx=0,
        )
        assert round_winner is None
        assert player_turn_over is False
        assert (
            game.players[slapping_player_idx].card_stack.nCards
            == expected_cards_after_penalty
        )
        assert game.round_stack.played_card_stack.nCards == 2
        assert game.round_stack.penalty_card_stack.nCards == 1

    def test_process_player_actions_stack_slapped_successfully(self, monkeypatch):
        """
        Test process_player_actions method of RatScrewGame when the stack is slapped successfully and won.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        slap_key = "b"
        user_inputs = iter(["a", slap_key, "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Setup round stack to be in a valid slap state
        game.round_stack.played_card_stack.add_card(Card("5", "hearts"))
        game.round_stack.played_card_stack.add_card(Card("5", "spades"))

        # Test slapping the stack
        slapping_player_idx = 0
        current_player_idx = 1
        round_winner, player_turn_over = game.process_player_actions(
            player_actions=slap_key,
            current_player_idx=current_player_idx,
            previous_player_idx=0,
        )
        assert round_winner == slapping_player_idx
        assert player_turn_over is True

    def test_process_player_actions_no_valid_actions(self, monkeypatch):
        """
        Test process_player_actions method of RatScrewGame when no valid actions are provided.
        """
        game = RatScrewGame()
        n_players = 2
        # Patch the built-in 'input' function to provide unique keys for each player
        user_inputs = iter(["a", "b", "c", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        game.setup_game(n_players)

        # Test processing player actions with no valid actions
        current_player_idx = 0
        previous_player_idx = 1
        round_winner, player_turn_over = game.process_player_actions(
            player_actions="xzy",  # invalid actions
            current_player_idx=current_player_idx,
            previous_player_idx=previous_player_idx,
        )
        assert round_winner is None
        assert player_turn_over is False
