# Stacc Discord Bot

A Discord bot that executes stack-based operations based on commands provided within backticks. The bot integrates with
a flask backend to process stack operations.

## Features

- Listens for messages containing "stacc" and code within backticks
- Executes stack-based operations through a REST API
- Displays both printed output and final stack state
- Error handling with informative messages

## Prerequisites

- Node.js (v20)
- Discord.js library
- CLIENT_SECRET environment variable set with discord client secret token.
- API Server running on localhost:8000 or domain specified in `API_URL` environment variable.

## Installation

1. Clone the repository
2. cd into the repository `cd staccbot/discord`
3. Install dependencies: `npm i`
4. Run the bot: `node index.js`

## Usage

Send messages containing "stacc" and code within backticks to the channel where the bot is active. The bot will execute
the code and respond with the printed output and final stack state.

### Example Usage:

Send discord message in channel where bot is active:
> stacc `10 DUP 5 LT IF THEN WHILE DUP 10 LT DO DUP PRINT 1 ADD END ELSE 1 10 2 FOR DUP PRINT END END`

### Output:

```
Results:
Printed output:
1
3
5
7
9

Final stack state: Stack([10, 1, 3, 5, 7, 9])
```