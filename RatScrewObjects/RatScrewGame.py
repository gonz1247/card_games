from CardDeckObjects import CardDeck
from RatScrewObjects.RoundCardStack import RoundCardStack
from RatScrewObjects.RatScrewPlayer import RatScrewPlayer


class RatScrewGame:
    """
    Class to run and manage gameplay state of Rat Screw card game
    """

    _MAX_CARDS = 52
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
        self.card_stack = CardDeck(nDecks=1)
        assert self.card_stack.nCards == self._MAX_CARDS

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
        # Play rounds until there is a winner
        winning_player = None
        player_start = 0
        stop_loop_count = 0
        while winning_player is None:
            player_start = self.play_round(starting_player=player_start)
            # check if someone won after round
            winning_player = self.check_for_winner()
        print(f"Player #{winning_player} has won the game!")

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
        initial_card_stacks = self.card_stack.deal_deck(nPiles=n_players)
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
        round_stack = RoundCardStack()
        print("--- New Round Starting ---")
        print(f"Player #{starting_player} goes first.")
        round_winner = None
        current_player = starting_player
        player_turn_over = False
        while round_winner is None:
            # Check to see if current player's turn is over
            if player_turn_over:
                print(f"Player #{current_player}, your turn is over.")
                current_player = self._get_next_elgible_player(current_player)
                print(f"Player #{current_player} is up.")

            # await player action(s)
            # player_actions = input("> ")

            # # update all card stacks based on player actions (play/slap)
            # round_winner, player_turn_over = self.update_card_stacks(
            #     round_stack, current_player, player_actions
            # )

            # check if current player's turn is over
            ## over if has no more cards --> (previous player wins stack)
            ## over if no more chances to play face-card --> (previous player wins stack)
            ## over if valid slap --> (slapping player wins stack)
            ## over if player played a face-card --> next player plays
            ## over if player played a non face-card when no face card was requried --> next player plays

            break  # placeholder to avoid infinite loop

        # Iterate through players turns until someone wins round
        print("~plays a round of rat screw~")
        # Move all cards to first player so that game ends (placeholder)
        self.players[0].card_stack = CardDeck(nDecks=1)
        for p_idx in range(1, len(self.players)):
            self.players[p_idx].card_stack = CardDeck(nDecks=0)
        self.card_stack = CardDeck(nDecks=0)
        return 0

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
        return next_player_idx
