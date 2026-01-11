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
        # Parameters for tracking players
        self.play_keys = dict()
        self.slap_keys = dict()
        self.players = list()
        # Parameters for tracking game state
        self.round_stack = RoundCardStack()
        self.game_winner = None
        self.round_winner = None
        self.player_turn_over = False

    def print_rules(self) -> None:
        """
        Print rat screw game rules to screen
        """
        print("Rat Screw Game Rules:")
        print(
            "1. Objective of the game is to be the first player to collect all the cards. Each player starts with an equal number of cards in their stack."
        )
        print(
            "2. Each round players take turns playing cards from their stack to the center pile."
        )
        print(
            "3. If a face card is played, the next player must play another face card within a certain number of tries (Ace=4 tries, King=3 tries, Queen=2 tries, Jack=1 try).\n   If they fail, the previous player wins the round and adds the center pile to their stack."
        )
        print(
            "4. Players can slap the pile when certain conditions are met to win the pile instantly.\n   Conditions for slapping are if the last two cards match in value (i.e., double) or if the last card matches the card two before it in value (i.e., sandwich)."
        )
        print("5. Each round starts with the player that won the previous round.")
        print("6. The game continues until one player has all the cards.")
        print()

    def print_controls_explanation(self) -> None:
        """
        Print rat screw game controls to screen
        """
        print("Rat Screw Game Controls:")
        print(
            "1. At the start of the game each player chooses two unique action keys, a play key and a slap key."
        )
        print("2. At any point of a round players can input any of their action keys.")
        print(
            "3. Once players have inputted action keys, hit 'enter' to submit player actions for processing."
        )
        print(
            "4. A player's play key will only be processed if it's their turn to play and will only be processed once per action submission."
        )
        print(
            "5. The action keys for each player will be printed out at the start of each round, along with the current number of cards they have"
        )
        print(
            "6. At any given time the player whose turn it is will be indicated by the number next to the action input reciever (i.e., P#>) "
        )
        print()

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
        self.game_winner = None
        self.round_winner = 0
        while self.game_winner is None:
            self.play_round(starting_player=self.round_winner)
            # check if someone won after round
            self.check_for_winner()
        print(f"Player #{self.game_winner} has won the game!")

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
        while fresh_deck.nCards > 0:
            self.round_stack.add_penalty_card(fresh_deck.deal_card())
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
        Play a single round of rat screw and update game state parameters

        Parameters
        ----------
        starting_player: int
            Index of player to start round
        """
        print("--- New Round Starting ---")
        # Show current card counts and controls for each player
        for p_idx, p in enumerate(self.players):
            print(
                f"Player #{p_idx} has {p.card_stack.nCards} cards. Play key: '{p.play_key}', Slap key: '{p.slap_key}'"
            )
        print(f"Player #{starting_player} goes first.")
        previous_player = None
        current_player = starting_player
        self.round_winner = None
        self.player_turn_over = False
        while self.round_winner is None:
            # Check to see if current player's turn is over
            if self.player_turn_over:
                previous_player = current_player
                current_player = self._get_next_elgible_player(current_player)
                self.player_turn_over = False

            # await player action(s)
            player_actions = input(f"P#{current_player}> ")

            # Process player actions and update game state
            self.process_player_actions(player_actions, current_player, previous_player)

        # Award round stack to round winner (get all penalty and played cards)
        print(f"Player #{self.round_winner} has won the round!")
        self.players[self.round_winner].take_round_stack(self.round_stack)

    def check_for_winner(self) -> None:
        """
        Update game_winner state based on if any player has collected all cards
        """
        self.game_winner = None
        # Iterate through players to see if anyone has all the cards
        for p_idx, p in enumerate(self.players):
            if p.card_stack.nCards == self._MAX_CARDS:
                self.game_winner = p_idx
                return

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
    ) -> None:
        """
        Update game state parameters based on player actions

        Parameters
        ----------
        player_actions: str
            String of player actions input
        current_player_idx: int
            Index of current player
        previous_player_idx: int
            Index of previous player
        """
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
                and not self.player_turn_over
            ):
                self.process_playing_card(current_player_idx, previous_player_idx)
                # Stop processing other player actions since card has been played
                break
            elif key in self.slap_keys:
                slapping_player_idx = self.slap_keys[key]
                self.process_slapping_stack(slapping_player_idx, current_player_idx)
                if self.round_winner is not None:
                    break

    def process_playing_card(
        self, current_player_idx: int, previous_player_idx: int
    ) -> None:
        """
        Update game state parameters based on current player playing card to round stack

        Parameters
        ----------
        current_player_idx: int
            Index of current player
        previous_player_idx: int
            Index of previous player
        """
        # Play a card from player's stack
        played_card = self.players[current_player_idx].play_card()
        self.round_stack.add_played_card(played_card)
        # Print card to screen
        print(played_card)
        # Determine if player's turn is over (satisfied current face card requirement)
        self.player_turn_over = (
            played_card.isFaceCard() or self.round_stack.need_face_card is False
        )
        # Check if round was been won
        if self.round_stack.has_stack_been_won() or (
            not self.player_turn_over
            and self.players[current_player_idx].card_stack.nCards < 1
        ):
            self.round_winner = previous_player_idx
            self.player_turn_over = True
        else:
            self.round_winner = None

    def process_slapping_stack(
        self, slapping_player_idx: int, current_player_idx: int
    ) -> None:
        """
        Update game state parameters based on player slapping round stack

        Parameters
        ----------
        slapping_player_idx: int
            Index of player who slapped the stack
        current_player_idx: int
            Index of current player
        """
        # Check if slap is valid and round was won
        if self.round_stack.is_valid_slap():
            print(f"Player #{slapping_player_idx} made a valid slap!")
            self.round_winner = slapping_player_idx
            return
        # Process an invalid slap
        print(f"Player #{slapping_player_idx} made an invalid slap!")
        # If slapper has no cards, they cannot pay penalty
        if self.players[slapping_player_idx].card_stack.nCards < 1:
            return
        # Provide penalty card for invalid slap
        self.round_stack.add_penalty_card(self.players[slapping_player_idx].play_card())
        # If currrent player check that they still have cards after penalty
        if slapping_player_idx == current_player_idx:
            self.player_turn_over = (
                self.players[current_player_idx].card_stack.nCards < 1
            )
