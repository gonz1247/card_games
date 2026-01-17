# Use image for running Python 3.10 applications
FROM python:3.13-slim

# Setting working directory inside the container
WORKDIR /card_games

# Copy Project files into the container
COPY CardDeck/__init__.py CardDeck/Card.py CardDeck/CardDeck.py CardDeck/
COPY RatScrew/__init__.py RatScrew/Game.py RatScrew/Player.py RatScrew/RoundCardStack.py  RatScrew/
COPY CardGamesMain.py .

# Run Card Games Main Program
CMD ["python", "CardGamesMain.py"]