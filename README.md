# fast-discordoauth2-api

FastAPI extension for Discord OAuth2 authentication.

## Features

- Easy Discord OAuth2 integration with FastAPI
- Full type hints and Pydantic models
- Supports all Discord OAuth2 scopes
- Handles token exchange and user info fetching
- Custom exceptions for Discord API errors

## Installation

```bash
git clone https://github.com/noxzion/fast-discordoauth2-api.git
pip install .
```

## Usage

```python
from fastapi import FastAPI, Request
from fast_discordoauth2_api.client import DiscordOAuth2Client
from fast_discordoauth2_api.models import DiscordOAuth2Config
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()

config = DiscordOAuth2Config(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8000/callback",
    scopes=["identify", "email", "guilds"],
)

discord_oauth = DiscordOAuth2Client(app, config)

@app.get("/login")
async def login():
    url = discord_oauth.get_authorization_url(state="random_state")
    return RedirectResponse(url)

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "Code not found"}, status_code=400)

    token_data = await discord_oauth.exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    if not access_token:
        return JSONResponse({"error": "Access token not found"}, status_code=400)

    user_info = await discord_oauth.get_user_info(access_token)
    return user_info
```
