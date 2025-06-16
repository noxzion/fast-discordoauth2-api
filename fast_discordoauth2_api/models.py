from typing import List, Literal

from pydantic import BaseModel, Field, HttpUrl, validator

DiscordScope = Literal[
    "activities.read",
    "activities.write",
    "applications.builds.read",
    "applications.builds.upload",
    "applications.commands",
    "applications.commands.update",
    "applications.commands.permissions.update",
    "applications.entitlements",
    "applications.store.update",
    "bot",
    "connections",
    "dm_channels.read",
    "email",
    "gdm.join",
    "guilds",
    "guilds.join",
    "guilds.members.read",
    "identify",
    "messages.read",
    "relationships.read",
    "role_connections.write",
    "rpc",
    "rpc.activities.write",
    "rpc.notifications.read",
    "rpc.voice.read",
    "rpc.voice.write",
    "voice",
    "webhook.incoming",
]


class DiscordOAuth2Config(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: HttpUrl
    scopes: List[DiscordScope] = Field(default_factory=lambda: ["identify", "email"])

    @validator("scopes", each_item=True)
    def validate_scopes(cls, v: str) -> str:
        if v not in DiscordScope.__args__:
            raise ValueError(f"Invalid Discord OAuth2 scope: {v}")
        return v
