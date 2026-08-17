# Hangman 🎯

## Description

Hangman is a full-stack, browser-based word game featuring multiple difficulty levels, family-friendly word lists, interactive feedback, and a persistent leaderboard. It uses Python, Flask, Gunicorn, NGINX, PostgreSQL, HTML, CSS, and PHP to deliver responsive gameplay across laptops, tablets, phones, and smart displays.

## Motivation

The goal was never to recreate a familiar word game; I wanted to turn something my nieces already loved into a game they could play on their own while teaching the younger kids. The dry-erase variant required a 'grown-up' to choose each word and manage every round, making independent play difficult. This project was born out of my own desire to automate the process and create a more engaging experience for everyone.

A quick transition from humble rounds of Hangman on a dry-erase board, coding started with a Bash terminal version we played together on a laptop. From there, I adapted the game for an Android tablet and eventually rebuilt it as a Flask web application.

Today, the kids play it through the web browser on a smart fridge.

Following the game from dry-erase board to terminal to web app gave me the opportunity to solve real usability and deployment challenges for real users. Most importantly, the kids still love playing it, making this project especially rewarding!

## Quick Start

1. Open [Hangman](https://hangman.gitbuzy.duckdns.org) in a modern web browser.
2. Choose a difficulty level.
3. Select letters and solve the word before the Hangman drawing is complete.

No installation is required to play the deployed version.

## Usage

1. Select a difficulty suited to the player.
2. Start a new round to receive a hidden word.
3. Choose letters using the on-screen controls.
4. Correct guesses reveal matching letters in the word.
5. Incorrect guesses advance the Hangman drawing.
6. Complete the word before running out of guesses.
7. Check the leaderboard, then start another round.

The responsive interface supports desktop and mobile browsers, Android tablets, and smart displays—including our family’s favorite: the fridge.

## Contributing

Contributions, bug reports, and suggestions are welcome. To build and run the application locally:

```bash
git clone <repository-url>
cd <repository-directory>

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

flask --app app run --debug
```

Open `http://127.0.0.1:5000` in your browser. The production application uses PostgreSQL for leaderboard data, so database-related changes require a local PostgreSQL configuration.

For production-style testing, run the app through Gunicorn:

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

When contributing:

1. Fork the repository and create a focused branch.
2. Keep word lists and player-facing messages family-friendly.
3. Test changes across desktop and mobile screen sizes.
4. Submit a pull request explaining the change and how it was tested.
