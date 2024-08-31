"""
ProtiumDB: Use your filesystem to build a database with rich interconnectivity between your data.
"""

from pydantic import Field

from .model import BaseModel

__all__ = [
    "BaseModel",
    "Field",
]
