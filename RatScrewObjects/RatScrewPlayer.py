from CardDeckObjects import CardDeck


class RatScrewPlayer:
    """
    Manage player state of participant in Rat Screw Game
    """

    def __init__(self, invalid_action_keys: set = None) -> None:
        """
        Intialize RatScrewPlayer instance and set desired keys for actions
        """
        if invalid_action_keys is None:
            invalid_action_keys = set()
        # play key (put card down)
        key_selection = input("Input key for playing cards by player: ")
        while not self.is_valid_action_key(key_selection, invalid_action_keys):
            print("Invalid action key, please try again")
            key_selection = input("Input key for playing cards by player: ")
        self.play_key = key_selection
        invalid_action_keys.add(key_selection)
        # slap key (slap card stack)
        key_selection = input("Input key for slapping card stack by player: ")
        while not self.is_valid_action_key(key_selection, invalid_action_keys):
            print("Invalid action key, please try again")
            key_selection = input("Input key for slapping card stack by player: ")
        self.slap_key = key_selection
        # player hand / card stack
        self.card_stack = CardDeck(nDecks=0)

    @staticmethod
    def is_valid_action_key(key: str, invalid_action_keys: set = None) -> bool:
        """
        Determine if key to use for player action is valid

        Parameters:
        -----------
        key: str,
            Character that player wants to use for one of their action keys
        invalid_action_keys: set, optional
            Set of action keys that should be seen as invalid options (default: None)

        Returns:
        -----------
        Boolean indicating whether key is a valid selection for an action key
        """
        if invalid_action_keys is None:
            invalid_action_keys = set()

        if key in invalid_action_keys:
            return False

        return len(key) == 1
