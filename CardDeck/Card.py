class Card:
    """
    A class representing a single playing card.
    """

    _valid_values = {
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "jack",
        "queen",
        "king",
        "ace",
    }

    _valid_suits = {"hearts", "diamonds", "clubs", "spades"}

    def __init__(self, value: str, suit: str) -> None:
        """
        Initializes a playing card with a value and suit.

        Parameters
        ----------
        value: str
            The value of the card (e.g., '2', '3', ..., '10', 'jack', 'queen', 'king', 'ace')
        suit: str
            The suit of the card (e.g., 'hearts', 'diamonds', 'clubs', 'spades')
        """
        self.value = value
        self.suit = suit

    @property
    def value(self) -> str:
        """
        Returns the value of the card.
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """
        Sets the value of the card.
        """
        if value.lower() not in self._valid_values:
            raise ValueError("Invalid card value")
        self._value = value.lower()

    @property
    def suit(self) -> str:
        """
        Returns the suit of the card.
        """
        return self._suit

    @suit.setter
    def suit(self, suit: str) -> None:
        """
        Sets the suit of the card.
        """
        if suit.lower() not in self._valid_suits:
            raise ValueError("Invalid card suit")
        self._suit = suit.lower()
