from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MIKROTIK_HOST: str
    MIKROTIK_USERNAME: str
    MIKROTIK_PASSWORD: str

    TAPO_USERNAME: str
    TAPO_PASSWORD: str
    TAPO_LIGHT_IP: str

    PIXO_REST_URL: str
    PIXO_REQUEST_DELAY: float = 0.8

    UBUNTU_USERNAME: str
    UBUNTU_PASSWORD: str

    INTRO_MUSIC_PATH: str
    OUTRO_MUSIC_PATH: str
    KILL_MUSIC_PATH: str
    DEATH_MUSIC_PATH: str

    BALANX_LED_MAC: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()

app_configs: dict[str, Any] = {
    'title': 'Druid Home Lab API',
    'description': 'Minimal Gateway API to ease the life of Druid',
    'swagger_ui_parameters': {'defaultModelsExpandDepth': -1},
}
