"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Fragrance(BaseModel):
    """
    Fragrances collection schema
    Collection name: "fragrance"
    """
    name: str = Field(..., description="Fragrance display name")
    slug: str = Field(..., description="URL-friendly unique identifier")
    sin: str = Field(..., description="One of the seven deadly sins this scent embodies")
    top_notes: List[str] = Field(default_factory=list, description="Top notes")
    heart_notes: List[str] = Field(default_factory=list, description="Heart notes")
    base_notes: List[str] = Field(default_factory=list, description="Base notes")
    description: str = Field(..., description="Short description of the fragrance")
    story: str = Field(..., description="Narrative story that accompanies the fragrance")
    price: float = Field(..., ge=0, description="Price in USD")
    image: Optional[str] = Field(None, description="Image URL")
    in_stock: bool = Field(True, description="Availability")

class Subscriber(BaseModel):
    """Email subscribers for announcements and drops"""
    email: EmailStr
    name: Optional[str] = None

class OrderItem(BaseModel):
    slug: str
    quantity: int = Field(ge=1, default=1)

class Order(BaseModel):
    """Simple order schema for preorders / reservations"""
    email: EmailStr
    name: Optional[str] = None
    items: List[OrderItem]
    notes: Optional[str] = None
