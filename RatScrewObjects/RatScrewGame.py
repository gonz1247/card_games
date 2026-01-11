from CardDeckObjects import CardDeck
from RatScrewObjects.RoundCardStack import RoundCardStack
from RatScrewObjects.RatScrewPlayer import RatScrewPlayer


class RatScrewGame:
    """
    Class to run and manage gameplay state of Rat Screw card game
    """

    _N_DECKS = 1
    _MAX_CARDS = _N_DECKS * 52
    _MAX_PLAYERS = _MAX_CARDS

    def __init__(self) -> None:
        """
        Initialize instance of RatScrewGame
        """
        self.reset_game_parameters()

    def reset_game_parameters(self) -> None:
        """
        Resets game parameters to initial/empty states
        """
        self.play_keys = dict()
        self.slap_keys = dict()
        self.players = list()
        self.round_stack = RoundCardStack()

    def play_game(self) -> None:
        """
        Play rat screw game
        """
        print("Starting new rat screw game")
        # Get number of players for the game
        n_players = self.get_number_of_players()
        print(f"{n_players} players are part of this game")
        # Setup game for players
        self.setup_game(n_players)
        # Play rounds until there is a winner for the game
        game_winner = None
        player_start = 0
        while game_winner is None:
            player_start = self.play_round(starting_player=player_start)
            # check if someone won after round
            game_winner = self.check_for_winner()
        print(f"Player #{game_winner} has won the game!")

    def get_number_of_players(self) -> int:
        """
        Ask user how many players will be part of game and validate input

        Returns
        -------
        Integer representing number of players requested
        """
        n_players = "dummy"
        while not n_players.isnumeric():
            n_players = input("How many players are part of this game? ")
        if int(n_players) > self._MAX_PLAYERS or int(n_players) < 2:
            print(f"Number of players must be between 2 and {self._MAX_PLAYERS}")
            return self.get_number_of_players()
        return int(n_players)

    def setup_game(self, n_players) -> None:
        """
        Setup rat screw game with n_players playing

        Parameters
        ----------
        n_players: int
            Number of players that will play rat screw game
        """
        # Check number of players
        if n_players > self._MAX_PLAYERS:
            raise ValueError(f"Maximum number of players is {self._MAX_PLAYERS}")
        self.reset_game_parameters()
        # Create initial stack for each player
        fresh_deck = CardDeck(nDecks=self._N_DECKS)
        initial_card_stacks = fresh_deck.deal_deck(nPiles=n_players)
        # Move left over cards from fresh deck to round stack penalty stack
        self.round_stack.penalty_card_stack = fresh_deck
        # initialize each player with stack of cards and action keys assigned
        for p_idx, p_card_stack in enumerate(initial_card_stacks):
            print(f"Setting up player #{p_idx}")
            # intialize player
            p = RatScrewPlayer(
                invalid_action_keys=(self.play_keys.keys() | self.slap_keys.keys())
            )
            # add action keys to dictionary to be able to reverse look up player index by their action keys
            self.play_keys[p.play_key] = p_idx
            self.slap_keys[p.slap_key] = p_idx
            # give player initial stack
            p.card_stack = p_card_stack
            # add player to game
            self.players.append(p)

    def play_round(self, starting_player: int) -> None:
        """
        Play a single round of rat screw

        Parameters
        ----------
        starting_player: int
            Index of player to start round

        Returns
        ----------
        Index of player to start next round
        """
        print("--- New Round Starting ---")
        # Show current card counts and controls for each player
        for p_idx, p in enumerate(self.players):
            print(
                f"Player #{p_idx} has {p.card_stack.nCards} cards. Play key: '{p.play_key}', Slap key: '{p.slap_key}'"
            )
        print(f"Player #{starting_player} goes first.")
        round_winner = None
        previous_player = None
        current_player = starting_player
        player_turn_over = False
        while round_winner is None:
            # Check to see if current player's turn is over
            if player_turn_over:
                previous_player = current_player
                current_player = self._get_next_elgible_player(current_player)

            # await player action(s)
            player_actions = input(f"P#{current_player}> ")

            # Process player actions and update their card stacks (play/slap)
            round_winner, player_turn_over = self.process_player_actions(
                player_actions, current_player, previous_player
            )

        # Award round stack to round winner (get all penalty and played cards)
        print(f"Player #{round_winner} has won the round!")
        self.players[round_winner].card_stack.combine_decks(
            self.round_stack.penalty_card_stack, onTop=False
        )
        self.players[round_winner].card_stack.combine_decks(
            self.round_stack.played_card_stack, onTop=False
        )

        # Reset round stack for next round
        self.round_stack = RoundCardStack()

        # Return index of round winner to start next round
        return round_winner

    def check_for_winner(self) -> int | None:
        """
        See if any player has won by collecting all cards

        Returns
        ----------
        Index of player who has won or None if no winner yet
        """
        # Iterate through players to see if anyone has all the cards
        for p_idx, p in enumerate(self.players):
            if p.card_stack.nCards == self._MAX_CARDS:
                return p_idx

    def _get_next_elgible_player(self, current_player_idx: int) -> int:
        """
        Get index of next player who has cards to play

        Parameters
        ----------
        current_player_idx: int
            Index of current player

        Returns
        ----------
        Index of next player with cards to play
        """
        n_players = len(self.players)
        next_player_idx = (current_player_idx + 1) % n_players
        while self.players[next_player_idx].card_stack.nCards == 0:
            next_player_idx = (next_player_idx + 1) % n_players
            if next_player_idx == current_player_idx:
                # No other players have cards
                break
        return next_player_idx

    def process_player_actions(
        self,
        player_actions: str,
        current_player_idx: int,
        previous_player_idx: int,
    ) -> tuple[int | None, bool]:
        """
        Process player actions for their turn

        Parameters
        ----------
        player_actions: str
            String of player actions input
        current_player_idx: int
            Index of current player
        previous_player_idx: int
            Index of previous player

        Returns
        ----------
        State of round after all player actions; tuple of (round winner index or None, boolean indicating if player's turn is over)
        """
        round_winner = None
        player_turn_over = False
        play_once_checker = set()
        # Placeholder logic for processing actions
        for key in player_actions:
            # Ensure each key is only processed once per turn
            if key in play_once_checker:
                continue
            play_once_checker.add(key)
            # Process action if key matches play or slap keys
            if (
                key == self.players[current_player_idx].play_key
                and not player_turn_over
            ):
                round_winner, player_turn_over = self.process_playing_card(
                    current_player_idx, previous_player_idx
                )
                # Stop processing other player actions since card has been played
                break
            elif key in self.slap_keys:
                slapping_player_idx = self.slap_keys[key]
                round_winner, player_turn_over = self.process_slapping_stack(
                    slapping_player_idx, current_player_idx
                )
                if round_winner is not None:
                    break
        return round_winner, player_turn_over

    def process_playing_card(
        self, current_player_idx: int, previous_player_idx: int
    ) -> int | None:
        """
        Process the current player playing a card

        Parameters
        ----------
        current_player_idx: int
            Index of current player
        previous_player_idx: int
            Index of previous player

        Returns
        ----------
        State of round after card has been played; tuple of (round winner index or None, boolean indicating if player's turn is over)
        """
        # Play a card from player's stack
        played_card = self.players[current_player_idx].play_card()
        self.round_stack.add_played_card(played_card)
        # Print card to screen
        print(played_card)
        # Determine if player's turn is over (satisfied current face card requirement)
        player_turn_over = (
            played_card.isFaceCard() or self.round_stack.need_face_card is False
        )
        # Check if round stack has been won by previous player (either no cards left or face card countdown expired)
        if self.round_stack.has_stack_been_won() or (
            not player_turn_over
            and self.players[current_player_idx].card_stack.nCards < 1
        ):
            round_winner = previous_player_idx
            player_turn_over = True
        else:
            round_winner = None
        return round_winner, player_turn_over

    def process_slapping_stack(
        self, slapping_player_idx: int, current_player_idx: int
    ) -> None:
        """
        Process a player slapping the round stack

        Parameters
        ----------
        slapping_player_idx: int
            Index of player who slapped the stack
        current_player_idx: int
            Index of current player

        Returns
        ----------
        State of round after stack has been slapped; tuple of (round winner index or None, boolean indicating if player's turn is over)
        """
        # Check if slap is valid and round was won
        if self.round_stack.is_valid_slap():
            print(f"Player #{slapping_player_idx} made a valid slap!")
            return slapping_player_idx, True
        # Process an invalid slap
        print(f"Player #{slapping_player_idx} made an invalid slap!")
        player_turn_over = False
        # If slapper has no cards, they cannot pay penalty
        if self.players[slapping_player_idx].card_stack.nCards < 1:
            return None, player_turn_over
        # Provide penalty card for invalid slap
        self.round_stack.add_penalty_card(self.players[slapping_player_idx].play_card())
        # If currrent player slapped check that they still have cards
        if slapping_player_idx == current_player_idx:
            player_turn_over = self.players[current_player_idx].card_stack.nCards < 1
        return None, player_turn_over
