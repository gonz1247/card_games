from CardDeckObjects import Card, CardDeck


class RoundCardStack:
    """
    Class to manage the stack of cards played during a round of Rat Screw
    """

    _face_card_countdown_cypher = {"jack": 1, "queen": 2, "king": 3, "ace": 4}

    def __init__(self) -> None:
        """
        Initialize instance of RoundCardStack
        """
        self.played_card_stack = CardDeck(nDecks=0)
        self.penalty_card_stack = CardDeck(nDecks=0)
        self.need_face_card = False
        self.face_card_countdown = 0

    def add_played_card(self, card: Card) -> None:
        """
        Play a card onto the round stack and update face card countdown if necessary

        Parameters
        ----------
        card: Card
            The card to be played onto the round stack.
        """
        self.played_card_stack.add_card(card)
        # Check if played card is a face card
        if card.isFaceCard():
            self.need_face_card = True
            self.face_card_countdown = self._face_card_countdown_cypher[card.value]
        else:
            self.face_card_countdown -= 1

    def add_penalty_card(self, card) -> None:
        """
        Add penalty cards to the penalty stack

        Parameters
        ----------
        card: Card
            Card to be added to the penalty stack.
        """
        self.penalty_card_stack.add_card(card)

    def has_stack_been_won(self) -> bool:
        """
        Determine stack has been won by a player

        Returns
        -------
        Boolean indicating whether the stack has been won
        """
        if self.need_face_card is False:
            return False
        return self.face_card_countdown < 1

    def is_valid_slap(self) -> bool:
        """
        Determine if slapping current stack is valid

        Returns
        -------
        Boolean indicating whether the stack is in a valid slap state
        """
        n_cards = self.played_card_stack.nCards
        if n_cards < 2:
            return False
        top_card = self.played_card_stack.see_card(0)
        second_card = self.played_card_stack.see_card(1)
        # Check for double
        if top_card.sameValue(second_card):
            return True
        # Check for sandwich
        if n_cards >= 3:
            third_card = self.played_card_stack.see_card(2)
            if top_card.sameValue(third_card):
                return True
        return False
