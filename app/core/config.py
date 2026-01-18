"""Application configuration with compatibility for pydantic v1 and v2.

This module attempts to locate a real `BaseSettings` class from either
the `pydantic` package (v1 or v2 export) or the `pydantic_settings`
package (v2 separate package). It validates the located symbol is a
class before using it as a base class.
"""

from typing import Any
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load variables from a local .env file into the process environment so
# BaseSettings can read them without needing to override `model_config`.
load_dotenv()


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "recycling_db"


settings: Any = Settings()
