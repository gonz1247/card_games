# Use image for running Python 3.10 applications
FROM python:3.13-slim

# Setting working directory inside the container
WORKDIR /card_games

# Do a local install of card_games package
COPY pyproject.toml .
COPY LICENSE . 
COPY README.md . 
COPY src/ .
RUN python -m pip install . 

# Copy script that will be ran in container
COPY DockerEntry.py . 

# Launch Card Games Runner
CMD ["python", "DockerEntry.py"]