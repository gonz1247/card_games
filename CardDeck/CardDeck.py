import random
from CardDeck import Card


class CardDeck:
    """
    A class representing a card deck containing one or more sets of standard 52 playing cards.
    """

    def __init__(self, nDecks: int = 1) -> None:
        """
        Initializes a standard card deck composed of one or more sets of 52 playing cards.

        Parameters
        ----------
        nDecks: int, optional
            The number of decks to include (default: 1)
        """
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
        for _ in range(nDecks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(value, suit))
        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffles the deck of cards.
        """
        random.shuffle(self.cards)

    def deal_card(self, fromBottom=False) -> Card:
        """
        Deals a single card from the deck.

        Returns
        -------
        Card object if available.
        """
        if len(self.cards) == 0:
            raise IndexError("No cards left in the deck")
        if fromBottom:
            return self.cards.pop(0)
        return self.cards.pop()

    def add_card(self, card: Card, onTop=False) -> None:
        """
        Adds a card into the deck.

        Parameters
        ----------
        card: Card
            The card to be added back to the deck.
        onTop: bool, optional
            If True, adds the card to the top of the deck; otherwise, adds it to the bottom (default: False)
        """
        if onTop:
            self.cards.append(card)
        else:
            self.cards.insert(0, card)

    def deal_deck(self, nPiles: int) -> list["CardDeck"]:
        """
        Deals the as much of the deck as possible into specified number of piles.

        Parameters
        ----------
        nPiles: int
            The number of piles to deal the deck into.

        Returns
        ----------
        A list of CardDeck objects, each containing an equal number of cards.
        """
        self.shuffle()
        piles = [CardDeck(nDecks=0) for _ in range(nPiles)]
        leftover = len(self.cards) % nPiles
        while len(self.cards) > leftover:
            for pile in piles:
                pile.add_card(self.deal_card(), onTop=True)
        return piles

    @property
    def nCards(self) -> int:
        """
        Returns the current number of cards in the deck.
        """
        return len(self.cards)
