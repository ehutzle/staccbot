# StaccBot - Discord Stack Language Interpreter

A Discord bot that executes stack-based operations through a Flask API backend. The bot listens for commands in Discord
and sends them to a Python-based API server for interpretation and execution.

## System Overview

The system consists of two main components:

1. **Discord Bot (Node.js)**
    - Listens for messages containing "stacc" and code within backticks
    - Forwards commands to the Flask API
    - Displays execution results back to Discord

2. **Stack Language Interpreter (Python Flask API)**
    - Interprets and executes stack-based operations
    - Handles arithmetic, conditionals, and loops
    - Returns execution results and final stack state

## Adding Bot to Discord Server

- Visit the following link to add the bot to your Discord
  server: [Add StaccBot to Discord](https://discord.com/oauth2/authorize?client_id=1312966708188938341)

## Stack Language Commands

### Basic Operations

- `PUSH <value>`: Push value onto stack
- `POP`: Pop value from stack
- `PRINT`: Pop and print value
- `ADD`, `SUB`, `MUL`, `DIV`: Basic arithmetic
- `DUP`: Duplicate top value
- `LT`, `GT`, `EQ`: Comparison operators

### Control Flow

- `IF`: `IF <condition> THEN <true_body> ELSE <false_body> END`
- `WHILE`: `WHILE <condition> DO <body> END`
- `FOR`: `FOR <start> <end> <step> DO <body> END`

## Installation & Setup

1. Clone the repository
2. Environment variables are configured in docker-compose.yml:

```yaml
services:
  discord:
    environment:
      - API_URL=http://server:8000
      - CLIENT_SECRET=your_discord_bot_token
```

3. Build and start services:

```bash
docker-compose build
docker-compose up
```

## API Response Details

The API response includes comprehensive information about the execution:

```json
{
  "prints": [
    "Array of all values printed during execution"
  ],
  "final_stack": "String representation of the final stack state",
  "status": "success or error",
  "error": "Error message if status is error (optional)"
}
```

## Docker Services

The project uses Docker Compose to manage two services:

1. `server`: Flask API service
    - Port: 8000

2. `discord`: Discord bot service
    - Depends on server service
    - Connects to Discord and Flask API

## Example Usage

> stacc \`10 DUP 5 LT IF THEN WHILE DUP 10 LT DO DUP PRINT 1 ADD END ELSE 1 10 2 FOR DUP PRINT END END`

> stacc \`1 10 1 FOR DUP PRINT END`

> stacc \`10 5 LT IF 1 ELSE 0 END`

> stacc \`1 0 DIV`