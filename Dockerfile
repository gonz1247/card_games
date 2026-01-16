# Use image for running Python 3.10 applications
FROM python:3.13-slim

# Setting working directory inside the container
WORKDIR /card_games

# Copy Project files into the container
COPY . .

# Run Card Games Main Program
CMD ["python", "CardGamesMain.py"]