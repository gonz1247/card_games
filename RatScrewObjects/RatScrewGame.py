import os
from CardDeckObjects import CardDeck
from RatScrewObjects import RatScrewPlayer


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
        # Clear console for new round
        # TODO: Maybe switch to just a print of new lines instead of clearing console
        os.system("cls" if os.name == "nt" else "clear")
        round_stack = CardDeck(nDecks=0)
        print(f"New round, player #{starting_player} goes first.")
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
