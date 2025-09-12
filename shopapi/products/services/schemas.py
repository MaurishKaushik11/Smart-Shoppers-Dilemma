from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional


class ProductOffer(BaseModel):
    price: Optional[float] = Field(default=None, description="Numeric price if parsed")
    currency: Optional[str] = Field(default=None)
    price_text: Optional[str] = Field(default=None, description="Raw price text if numeric parsing failed")
    seller: Optional[str] = Field(default=None)
    link: Optional[str] = Field(default=None)


class ProductCard(BaseModel):
    name: str
    brand: Optional[str] = None
    total_weight: Optional[str] = Field(default=None, description="e.g., 16 oz, 500 g")
    offers: List[ProductOffer] = Field(default_factory=list)
    source: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    results: List[ProductCard]
    sources_used: List[str] = Field(default_factory=list)