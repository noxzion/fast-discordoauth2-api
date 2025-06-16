from typing import Any, Dict, Optional, Union

from fastapi import FastAPI
from .HTTPSession import DiscordOAuth2Session

from .models import DiscordOAuth2Config


class DiscordOAuth2Client:
    def __init__(self, app: FastAPI, config: DiscordOAuth2Config) -> None:
        self.app = app
        self.config = config
        self.session = DiscordOAuth2Session()

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        scope_str = " ".join(self.config.scopes)
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": str(self.config.redirect_uri),
            "response_type": "code",
            "scope": scope_str,
        }
        if state:
            params["state"] = state
        query = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{self.session.authorization_url}?{query}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        return await self.session.exchange_code_for_token(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            code=code,
            redirect_uri=str(self.config.redirect_uri),
            scopes=" ".join(self.config.scopes),
        )

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        return await self.session.get_user_info(access_token)

    async def get(
        self,
        auth_url: bool = False,
        token: Optional[str] = None,
        state: Optional[str] = None,
        is_access_token: bool = False,
    ) -> Union[str, Dict[str, Any]]:
        if auth_url:
            return self.get_authorization_url(state=state)
        if token:
            if is_access_token:
                return await self.get_user_info(token)
            return await self.exchange_code_for_token(token)
        raise ValueError("Either auth_url=True or token must be provided")
