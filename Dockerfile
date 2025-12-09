# Use image for running Python 3.10 applications
FROM python:3.10-slim

# Setting working directory inside the container
WORKDIR /card_games

# Install required Python packages
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy Project files into the container
COPY . .

# Run Card Games Main Program
CMD ["python", "CardGamesMain.py"]