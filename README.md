# Flask Hangman 🎯

A family-friendly Hangman web app built with Python and Flask.

This project began as a terminal game I wrote for my kids. We first played it together on a laptop through Bash, then moved it to an Android tablet. After rebuilding it as a Flask web app, the game made its way to its most important platform yet: **the web browser on our smart fridge**.

The kids love playing it, and watching a simple terminal project grow into a family favorite has made this one especially fun to build.

## Features

- Multiple difficulty levels for kids and adults
- Family-friendly word lists
- Fun feedback for correct and incorrect guesses
- Browser-based gameplay across computers, tablets, and smart displays
- Persistent score leaderboard

## Stack

- **Python** and **Flask** power the application
- **Gunicorn** serves the production app
- **NGINX** handles reverse proxying and HTTPS
- **PostgreSQL** stores leaderboard scores
- **HTML, CSS, and JavaScript** provide the browser interface

## Run Locally

```bash
git clone <repository-url>
cd <repository-directory>

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

flask --app app run --debug
```

Open `http://127.0.0.1:5000` in your browser and start guessing.

## Production

The deployed version runs behind NGINX using Gunicorn as the WSGI server.

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

---

Built for the kids, tested on the fridge. ❤️
