# Quizzify :musical_score:

Are you a music expert? Quizzify will challenge your musical knowledge. Quizzify invites music enthusiasts to test their expertise! Delve into a challenging and fun quiz experience designed to push your musical knowledge to the limit.

## Quick start

### Installation

```bash
git clone git@github.com:alannadevgen/quizzify.git
cd quizzify
python3 -m venv venv
source venv/bin/activate
# python3 main.py
```

## Local setup

1. Set the environment variables in an `.env` file in the root directory of the project. The `.env` file should contain the following variables:

```shell
SPOTIFY_CLIENT_ID=<YOUR SPOTIFY CLIENT ID>  # TBD
SPOTIFY_CLIENT_SECRET=<YOUR SPOTIFY CLIENT SECRET>  # TBD
SPOTIFY_REDIRECT_URI=<YOUR REDIRECT URI AS DEFINED IN YOUR SPOTIFY DASHBOARD APP> # TBD
SPOTIFY_AUTH_URL=https://accounts.spotify.com/authorize
SPOTIFY_TOKEN_URL=https://accounts.spotify.com/api/token
SPOTIFY_AUTH_SCOPE="LIST OF SCOPES TO DEFINE"  # TBD
```

2. Pre-commit hooks:

Pre-commit hooks have been defined to ensure a good code quality. To enable these pre-commit hooks, the following commands should be executed.

```shell
pip install pre-commit
pre-commit install # set up the git hook scripts
```

3. Build & Run the docker image using Docker.

````shell
docker build -t quizzify .
docker run -it --rm --name quizzify -p 8000:8000 quizzify
````

You can now access the application at http://localhost:8000.

## Architecture

TBD

## Contributors :woman_technologist:

<a href="https://github.com/alannadevgen/quizzify/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=alannadevgen/quizzify" />
</a>