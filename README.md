# Discord RAG Chatbot

## Overview

This is a Python-based Discord chatbot that leverages Retrieval-Augmented Generation (RAG) to provide responses based on Serbian history. The bot utilizes Astra DB to store and query vector embeddings generated from historical documents.

## Features

- Uses files about Serbian history to create an embedded vector table in Astra DB.
- Implements a `/ask` command in Discord to query the database and return AI-generated responses.
- Dockerized for easy deployment.
- Supports execution via Python, VS Code (`launch.json`), and Docker Compose.

## Setup and Installation

### Prerequisites

- Python 3.x (3.12 used in development process)
- Docker & Docker Compose
- Astra DB account
- Discord bot token

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd discord-rag-chatbot
   ```

2. **Install dependencies**:

   Recommend using venv

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file and add the following:

   ```env
   DISCORD_BOT_TOKEN=your_discord_token
   ASTRA_DB_ID=your_astra_db_id
   ASTRA_DB_REGION=your_astra_db_region
   ASTRA_DB_KEYSPACE=your_astra_db_keyspace
   ```

4. **Run the bot locally**:
   ```bash
   python bot.py
   ```

## Running with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t discord-rag-bot .
   ```
2. **Run the container**:
   ```bash
   docker run --env-file .env discord-rag-bot
   ```

## Running with Docker Compose

1. **Start the bot**:
   ```bash
   docker-compose up -d
   ```
2. **Stop the bot**:
   ```bash
   docker-compose down
   ```

## Running with VS Code Debugger

Ensure that `launch.json` is configured correctly and run the bot from VS Code's debugging panel.

## Usage

- Once the bot is running, use the `/ask` command in a Discord server where the bot is added.
- The bot retrieves relevant historical information from Astra DB and generates responses.

## Contributing

Pull requests and issues are welcome! Please follow standard coding practices and ensure proper documentation.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact me on github or open an issue in the repository.
