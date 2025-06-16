from typing import Any, Dict

import httpx

from .exceptions import (
    DiscordAPIHTTPException,
    DiscordOAuth2Exception,
)


class DiscordOAuth2Session:
    authorization_url: str = "https://discord.com/api/oauth2/authorize"
    token_url: str = "https://discord.com/api/oauth2/token"
    api_base_url: str = "https://discord.com/api"

    async def exchange_code_for_token(
        self,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
        scopes: str,
    ) -> Dict[str, Any]:
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "scope": scopes,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise DiscordAPIHTTPException(
                status_code=e.response.status_code,
                detail=e.response.text,
                original_exception=e,
            ) from e
        except Exception as e:
            raise DiscordOAuth2Exception(
                "Unexpected error while exchanging code for token", original_exception=e
            ) from e

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_base_url}/users/@me", headers=headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise DiscordAPIHTTPException(
                status_code=e.response.status_code,
                detail=e.response.text,
                original_exception=e,
            ) from e
        except Exception as e:
            raise DiscordOAuth2Exception(
                "Unexpected error while fetching user info", original_exception=e
            ) from e
